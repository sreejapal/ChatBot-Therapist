import os
os.environ["POSTHOG_API_KEY"] = "disabled"

print("=== LAUNCHER_API.PY IS RUNNING ===")
from flask import Flask, request, jsonify, send_from_directory, abort, session
from flask_cors import CORS
import subprocess
import sys
import os
import psutil
from app.logic import process_user_input
from app.memory import clear_memory, search_memory, get_all_sessions, analyze_history_with_langchain, start_new_session, get_last_session_id, get_session_logs
from assets.dashboard import generate_weekly_summary, generate_monthly_summary, generate_overall_summary

app = Flask(__name__, static_folder='frontend')
app.secret_key = 'your-secret-key-here'  # Required for session management
CORS(app)

# Map dashboard names to script filenames and ports
DASHBOARDS = {
    'weekly':  {'script': 'dashboard_weekly.py',  'port': 7861},
    'monthly': {'script': 'dashboard_monthly.py', 'port': 7862},
    'overall': {'script': 'dashboard_overall.py', 'port': 7863},
    'search':  {'script': 'search_app.py',        'port': 7864},
}

def is_port_in_use(port):
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port:
            return True
    return False

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # Only serve files with allowed extensions
    allowed_exts = ('.html', '.js', '.css', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.json')
    if any(path.endswith(ext) for ext in allowed_exts):
        return send_from_directory('frontend', path)
    abort(404)

@app.route('/api_chat', methods=['POST'])
def api_chat():
    print("Received /api_chat request")
    try:
        data = request.get_json(force=True, silent=True)
        print("Request data:", data)
        if not data or 'user_input' not in data:
            return jsonify({"error": "Missing user_input"}), 400
        
        user_input = data['user_input'].strip()
        if not user_input:
            return jsonify({"error": "User input cannot be empty"}), 400
            
        # Limit input length for security
        if len(user_input) > 2000:
            return jsonify({"error": "Message too long. Please keep it under 2000 characters."}), 400
            
        print("User input:", user_input)
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        # Use Flask session for better session management
        if 'session_history' not in session:
            session['session_history'] = []
        
        print("Calling process_user_input")
        result = process_user_input(user_input, session['session_history'])
        print("process_user_input returned")
        session['session_history'].append([user_input, result["reflection"]])
        
        return jsonify({
            "reflection": result["reflection"],
            "questions": result.get("questions", []),
            "suggestions": result.get("suggestions", [])
        })
    except Exception as e:
        print(f"Error processing user input: {e}")
        return jsonify({
            "error": "Sorry, there was an error processing your message. Please try again.",
            "reflection": "I apologize, but I'm having trouble processing your message right now. Could you please try again?",
            "questions": ["Are you still there?", "Would you like to try rephrasing your message?"],
            "suggestions": ["Take a moment to breathe and try again when you're ready."]
        }), 500

@app.route('/reset', methods=['POST'])
def reset_api():
    print("Received /reset request")
    session['session_history'] = []
    clear_memory()
    return '', 204

@app.route('/new_session', methods=['POST'])
def new_session_api():
    """Start a new therapy session"""
    print("Received /new_session request")
    session['session_history'] = []
    # Don't clear memory, just start fresh session
    return jsonify({"status": "new session started", "session_id": start_new_session()})

@app.route('/current_session')
def current_session_api():
    """Get current session information"""
    session_history = session.get('session_history', [])
    current_session_id = get_last_session_id()
    return jsonify({
        "session_id": current_session_id,
        "message_count": len(session_history),
        "is_active": len(session_history) > 0
    })

@app.route('/summary')
def summary_api():
    summary_type = request.args.get('type')
    if summary_type == 'weekly':
        summary, img = generate_weekly_summary()
    elif summary_type == 'monthly':
        summary, img = generate_monthly_summary()
    elif summary_type == 'overall':
        summary, img = generate_overall_summary()
    else:
        return jsonify({"summary": "Invalid summary type.", "img": None})
    return jsonify({"summary": summary, "img": img})

@app.route('/search', methods=['POST'])
def search_api():
    query = request.json['query']
    results = search_memory(query)
    if not results:
        return jsonify({"results": "No matching results found."})
    return jsonify({"results": '\n\n'.join([f"🧍 {u}\n🤖 {b}" for u, b in results])})

@app.route('/launch_dashboard', methods=['POST'])
def launch_dashboard():
    dashboard = request.json.get('dashboard')
    if dashboard not in DASHBOARDS:
        return jsonify({'status': 'unknown dashboard'}), 400
    script = DASHBOARDS[dashboard]['script']
    port = DASHBOARDS[dashboard]['port']
    if not is_port_in_use(port):
        # Launch the dashboard script
        subprocess.Popen([sys.executable, script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return jsonify({'status': 'launched', 'port': port})

@app.route('/history')
def history_api():
    sessions = get_all_sessions()
    return jsonify({"sessions": sessions})

@app.route('/session_summaries')
def session_summaries_api():
    """Get only the first message from each session for summary view"""
    sessions = get_all_sessions()
    summaries = {}
    for sid, session_logs in sessions.items():
        # Get only user messages and find the first one
        user_messages = [log for log in session_logs if log.get('message_type') == 'user']
        if user_messages:
            first_message = user_messages[0]
            summaries[sid] = {
                'first_message': first_message.get('user_input', ''),
                'timestamp': first_message.get('timestamp', ''),
                'emotion': first_message.get('emotion', 'unknown'),
                'message_count': len(session_logs)
            }
    return jsonify({"summaries": summaries})

@app.route('/session/<session_id>')
def session_detail_api(session_id):
    """Get full conversation for a specific session"""
    session_logs = get_session_logs(session_id)
    if not session_logs:
        return jsonify({"error": "Session not found"}), 404
    
    # Format the conversation with both user and bot messages
    conversation = []
    for log in session_logs:
        conversation.append({
            'timestamp': log.get('timestamp', ''),
            'message': log.get('user_input', ''),
            'type': log.get('message_type', 'user'),
            'emotion': log.get('emotion', 'unknown') if log.get('message_type') == 'user' else None
        })
    
    return jsonify({"session_id": session_id, "conversation": conversation})

@app.route('/search_sessions', methods=['POST'])
def search_sessions_api():
    """Search and return session summaries that match the query"""
    query = request.json.get('query', '')
    if not query:
        return jsonify({"summaries": {}})
    
    # Get all sessions
    sessions = get_all_sessions()
    matching_summaries = {}
    
    for sid, session_logs in sessions.items():
        # Check if any message in the session matches the query
        session_matches = False
        first_message = ""
        first_timestamp = ""
        first_emotion = "unknown"
        
        for log in session_logs:
            if log.get('message_type') == 'user':
                user_input = log.get('user_input', '').lower()
                if query.lower() in user_input:
                    session_matches = True
                    if not first_message:  # Get the first message for summary
                        first_message = log.get('user_input', '')
                        first_timestamp = log.get('timestamp', '')
                        first_emotion = log.get('emotion', 'unknown')
        
        if session_matches and first_message:
            matching_summaries[sid] = {
                'first_message': first_message,
                'timestamp': first_timestamp,
                'emotion': first_emotion,
                'message_count': len(session_logs)
            }
    
    return jsonify({"summaries": matching_summaries})

@app.route('/analyze', methods=['POST'])
def analyze_api():
    data = request.json
    question = data.get('question')
    session_id = data.get('session_id')
    days = data.get('days')
    answer = analyze_history_with_langchain(question, session_id=session_id, days=days)
    return jsonify({"answer": answer})

@app.route('/test', methods=['POST'])
def test_api():
    print("Received /test request")
    return "OK", 200

if __name__ == "__main__":
    import threading
    import time
    import webbrowser

    def run_flask():
        app.run(debug=True, use_reloader=False)

    # Start Flask app in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Wait a moment to ensure the Flask server is up
    time.sleep(2)
    print("Flask backend launched.")
    print("Open your app in a browser:")
    print("  http://127.0.0.1:5000/index.html (Chat)")
    print("  http://127.0.0.1:5000/weekly.html (Weekly Dashboard)")
    print("  http://127.0.0.1:5000/monthly.html (Monthly Dashboard)")
    print("  http://127.0.0.1:5000/overall.html (Overall Dashboard)")
    print("  http://127.0.0.1:5000/search.html (Search & History)")
    # Automatically open the main chat page
    webbrowser.open_new("http://127.0.0.1:5000/index.html")

    # Keep the main thread alive while the Flask app runs
    flask_thread.join() 