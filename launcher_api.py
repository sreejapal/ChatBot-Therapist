from flask import Flask, request, jsonify
import subprocess
import sys
import os
import psutil

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(port=5000) 