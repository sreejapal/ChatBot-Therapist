def detect_emotion(user_input):
    try:
        allowed_emotions = [
            "happy", "sad", "anxious", "angry", "lonely", "excited", "depressed",
            "grateful", "hopeful", "joy", "love", "good", "great", "better", "improved",
            "bad", "worse", "hopeless", "tired", "down"
        ]
        prompt = f"""Identify the primary emotion in the following sentence:
        "{user_input}"
        Respond with only one word from: {', '.join(allowed_emotions)}"""
        from models.ollama_runner import load_llm
        llm = load_llm()
        response = llm.generate([prompt.strip()])
        generated_emotion = response.generations[0][0].text.strip().lower()
        emotion = generated_emotion if generated_emotion in allowed_emotions else "unknown"
        # Try to recover if emotion is unknown
        attempts = 0
        while emotion == "unknown" and attempts < 2:
            follow_up = f"""The emotion wasn't clear from this message:
        {user_input}
        Politely ask the user to describe the situation in more detail so we can better understand their feelings. Respond with only one word from: {', '.join(allowed_emotions)}"""
            followup_response = llm.generate([follow_up.strip()])
            followup_emotion = followup_response.generations[0][0].text.strip().lower()
            if followup_emotion in allowed_emotions:
                emotion = followup_emotion
                break
            attempts += 1
        return emotion
    except Exception as e:
        print(f"[ERROR] Exception in detect_emotion: {e}")
        # Fallback to basic emotion detection
        text_lower = user_input.lower()
        if any(word in text_lower for word in ["happy", "good", "great", "excited", "joy"]):
            return "happy"
        elif any(word in text_lower for word in ["sad", "bad", "depressed", "down"]):
            return "sad"
        elif any(word in text_lower for word in ["anxious", "worried", "nervous"]):
            return "anxious"
        elif any(word in text_lower for word in ["angry", "mad", "frustrated"]):
            return "angry"
        else:
            return "unknown"

def simple_sentiment_score(text):
    # Very basic sentiment: +1 for positive, -1 for negative, 0 for neutral
    positive_words = ["happy", "excited", "grateful", "hopeful", "joy", "love", "good", "great", "better", "improved"]
    negative_words = ["sad", "angry", "anxious", "depressed", "bad", "worse", "hopeless", "lonely", "tired", "down"]
    score = 0
    for word in positive_words:
        if word in text.lower():
            score += 1
    for word in negative_words:
        if word in text.lower():
            score -= 1
    return max(-1, min(1, score))  # Clamp to -1, 0, 1 