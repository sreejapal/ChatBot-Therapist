# LangChain chains and reasoning logic
from models.ollama_runner import load_llm
import re
from app.memory import save_to_memory
from app.utils import detect_emotion, simple_sentiment_score


llm=load_llm()

def analyze_emotion(user_input, history):
    print("[DEBUG] Entering analyze_emotion")
    try:
        context = ""
        for user_msg, bot_msg in history:
            context += f"User: {user_msg}\nBot: {bot_msg}\n"
        prompt = f"""
You are a compassionate, professional therapist AI. Your job is to help the user reflect deeply, feel emotionally supported, and gently guided.

Here is the conversation so far:
{context}

The user just said: "{user_input}"

Now respond with:
Reflection: (a warm, deeply empathetic reflection on their message, acknowledging their feelings and thoughts, ideally 7-8 sentences long, using human-like language and emotional intelligence)
Questions: (2–3 thoughtful, open-ended follow-up questions that encourage deeper understanding and self-reflection, each on a new line. Make these questions feel caring, supportive, and non-judgmental.)
Suggestions: (After the questions, provide 1–2 suggestions for healing activities, coping strategies, or mental exercises. These suggestions should be based on clinically proven, evidence-based psychological or medical practices—such as CBT, mindfulness, journaling, or behavioral activation. If possible, mention if a suggestion has a history of working for many people. Make the suggestions feel gentle, supportive, and practical.)

Keep your tone soft, respectful, and emotionally intelligent. Do not provide suggestions until after the follow-up questions.
Only provide text—no labels or markdown. You can use the following format:
Reflection: [Your reflection here]
Questions:[Your questions here, each on a new line]
Suggestions: [Your suggestions here, each on a new line]

"""
        print("[DEBUG] About to call llm.generate")
        response = llm.generate([prompt.strip()])
        print("[DEBUG] llm.generate completed successfully")
        generated_text = response.generations[0][0].text
        print("[DEBUG] Exiting analyze_emotion")
        return generated_text
    except Exception as e:
        print(f"[ERROR] Exception in analyze_emotion: {e}")
        # Return a fallback response if Ollama fails
        return f"""Reflection: I understand you're reaching out, and I want to be here for you. It seems like you're looking for support and understanding right now. I'm here to listen and help you process whatever you're going through. Your feelings are valid, and it's okay to share them. Sometimes just expressing ourselves can be the first step toward feeling better. I want you to know that you're not alone in this journey.

Questions:
What's been on your mind lately that you'd like to talk about?
How have you been feeling emotionally over the past few days?
What would be most helpful for you right now - someone to listen, practical advice, or just a safe space to express yourself?

Suggestions:
Consider taking a few deep breaths and checking in with yourself about what you need most right now. Many people find that simple mindfulness exercises can help create a sense of calm and clarity.
You might also find it helpful to write down your thoughts and feelings in a journal, as this can often help us process our emotions and gain new insights."""

def process_user_input(user_input, history, session_id=None):
    print(f"[DEBUG] Entering process_user_input with user_input: {user_input}")
    history = [list(pair) for pair in history]
    response = analyze_emotion(user_input, history)
    emotion = detect_emotion(user_input)
    sentiment_score = simple_sentiment_score(user_input)
    try:
        parts = response.split('Questions:')
        reflection = parts[0].replace('Reflection:', '').strip() if len(parts) > 1 else response
        rest = parts[1] if len(parts) > 1 else ''
        questions_part, suggestions_part = rest.split('Suggestions:') if 'Suggestions:' in rest else (rest, '')
        questions = [q.strip('- ').strip() for q in questions_part.strip().split('\n') if q.strip()]
        suggestions = [s.strip('- ').strip() for s in suggestions_part.strip().split('\n') if s.strip()]
    except Exception as e:
        print(f"[DEBUG] Exception in parsing response: {e}")
        # Fallback: try regex to extract questions
        pattern = r"[Qq]uestions[:\s]*\n(?:[-*\u2022] ?.*\n?)+"
        match = re.search(pattern, response)
        if match:
            questions_text = match.group()
            questions = [q.strip('- ').strip() for q in questions_text.split('\n') if q.strip() and not q.lower().startswith('questions')]
        else:
            questions = []
        suggestions_pattern = r"[Ss]uggestions[:\s]*\n(?:[-*\u2022] ?.*\n?)+"
        suggestions_match = re.search(suggestions_pattern, response)
        if suggestions_match:
            suggestions_text = suggestions_match.group()
            suggestions = [s.strip('- ').strip() for s in suggestions_text.split('\n') if s.strip() and not s.lower().startswith('suggestions')]
        else:
            suggestions = []
        
        reflection = response
    history.append([user_input, reflection])  # Save as list, not tuple
    # Log user message
    save_to_memory(user_input, emotion, session_id=session_id, sentiment_score=sentiment_score, message_type="user")
    # Log bot reflection
    save_to_memory(reflection, None, session_id=session_id, sentiment_score=None, message_type="bot")
    print("[DEBUG] Exiting process_user_input")
    return {
        "reflection": reflection,
        "questions": questions,
        "suggestions": suggestions
    }
