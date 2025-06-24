# LangChain chains and reasoning logic
from models.ollama_runner import load_llm
import re
from app.memory import save_to_memory


llm=load_llm()

def detect_emotion(text):
    # Simple example – improve with LLM later
    for emotion in ["sad", "happy", "anxious", "angry", "lonely", "excited", "depressed"]:
        if emotion in text.lower():
            return emotion
    return "unknown"

def analyze_emotion(user_input, history):
    context = ""
    for user_msg, bot_msg in history:
        context += f"User: {user_msg}\nBot: {bot_msg}\n"
    prompt = f"""
You are a compassionate therapist AI. Your job is to help the user reflect deeply, feel emotionally supported, and gently guided.

Here is the conversation so far:
{context}

The user just said: "{user_input}"

Now respond with:
Reflection: (a warm, empathetic reflection on their message, acknowledging their feelings and thoughts, ideally 7-8 sentences long and a bit detailed)
Questions: (2–3 thoughtful follow-up questions that encourage deeper understanding, each on a new line)
Suggestions: (1–2 healing activities or mental exercises they could try, each on a new line)

Keep your tone soft, respectful, and emotionally intelligent.
Only provide text—no labels or markdown. You can use the following format:
Reflection: [Your reflection here]
Questions:[Your questions here, each on a new line]
Suggestions: [Your suggestions here, each on a new line]

"""

    response = llm.generate([prompt.strip()])
    generated_text = response.generations[0][0].text
    return generated_text

def process_user_input(user_input, history):
    # Ensure history is a list of lists (not tuples)
    history = [list(pair) for pair in history]
    response = analyze_emotion(user_input, history)
    emotion = detect_emotion(user_input)
    try:
        # Try to extract questions using regex if standard split fails
        parts = response.split('Questions:')
        reflection = parts[0].replace('Reflection:', '').strip() if len(parts) > 1 else response
        rest = parts[1] if len(parts) > 1 else ''
        questions_part, suggestions_part = rest.split('Suggestions:') if 'Suggestions:' in rest else (rest, '')
        questions = [q.strip('- ').strip() for q in questions_part.strip().split('\n') if q.strip()]
        suggestions = [s.strip('- ').strip() for s in suggestions_part.strip().split('\n') if s.strip()]
    except Exception:
        # Fallback: try regex to extract questions
        pattern = r"[Qq]uestions[:\s]*\n(?:[-*•] ?.*\n?)+"
        match = re.search(pattern, response)
        if match:
            questions_text = match.group()
            questions = [q.strip('- ').strip() for q in questions_text.split('\n') if q.strip() and not q.lower().startswith('questions')]
        else:
            questions = []
        # You can similarly use regex for suggestions if needed
        reflection = response
        suggestions = []
    history.append([user_input, reflection])  # Save as list, not tuple
    save_to_memory(user_input, emotion)

    return {
        "reflection": reflection,
        "questions": questions,
        "suggestions": suggestions
    }
