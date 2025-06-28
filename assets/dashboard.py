import os
import json
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from models.ollama_runner import load_llm

LOG_FILE = "data/emotion_log.json"

llm = load_llm()

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def filter_logs_by_days(logs, days):
    cutoff = datetime.now() - timedelta(days=days)
    return [log for log in logs if datetime.fromisoformat(log["timestamp"]) >= cutoff]

def get_summary(logs):
    total = len(logs)
    counter = Counter(log["emotion"] for log in logs)
    summary_text = f"Total conversations: {total}\nMost common emotions:\n"
    for emotion, count in counter.most_common():
        summary_text += f"- {emotion}: {count}\n"
    return summary_text

def plot_emotion_graph(logs, filename):
    counter = Counter(log["emotion"] for log in logs)
    if not counter:
        return None  # Nothing to plot

    emotions = list(counter.keys())
    counts = list(counter.values())

    plt.figure(figsize=(5, 3))
    plt.bar(emotions, counts, color="teal")
    plt.title("Emotion Frequency")
    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def plot_sentiment_over_time(logs, filename, window=1, period='day'):
    if not logs:
        return None
    df = pd.DataFrame([
        {
            'timestamp': log['timestamp'],
            'sentiment_score': log.get('sentiment_score'),
            'message_type': log.get('message_type', 'user')
        }
        for log in logs if log.get('sentiment_score') is not None and log.get('message_type') == 'user'
    ])
    if df.empty:
        return None
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if period == 'day':
        df['period'] = df['timestamp'].dt.date
    elif period == 'week':
        df['period'] = df['timestamp'].dt.to_period('W').apply(lambda r: r.start_time.date())
    elif period == 'month':
        df['period'] = df['timestamp'].dt.to_period('M').apply(lambda r: r.start_time.date())
    else:
        df['period'] = df['timestamp'].dt.date
    grouped = df.groupby('period')['sentiment_score'].mean()
    rolling = grouped.rolling(window=window, min_periods=1).mean()
    plt.figure(figsize=(6, 3))
    plt.plot(grouped.index, grouped.values, label='Avg Sentiment')
    plt.plot(rolling.index, rolling.values, label=f'Rolling Avg ({window})')
    plt.title('Sentiment Score Over Time')
    plt.xlabel(period.capitalize())
    plt.ylabel('Sentiment Score')
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def summarize_trends(logs, period='month'):
    if not logs:
        return "No data for trend analysis."
    df = pd.DataFrame([
        {
            'timestamp': log['timestamp'],
            'sentiment_score': log.get('sentiment_score'),
            'emotion': log.get('emotion'),
            'message_type': log.get('message_type', 'user')
        }
        for log in logs if log.get('sentiment_score') is not None and log.get('message_type') == 'user'
    ])
    if df.empty:
        return "No user sentiment data."
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if period == 'month':
        df['period'] = df['timestamp'].dt.to_period('M').apply(lambda r: r.start_time.date())
    elif period == 'week':
        df['period'] = df['timestamp'].dt.to_period('W').apply(lambda r: r.start_time.date())
    else:
        df['period'] = df['timestamp'].dt.date
    grouped = df.groupby('period')['sentiment_score'].mean()
    if len(grouped) < 2:
        return "Not enough data for trend analysis."
    change = grouped.iloc[-1] - grouped.iloc[0]
    trend = "improved" if change > 0 else "declined" if change < 0 else "remained stable"
    return f"Your average sentiment has {trend} from {grouped.iloc[0]:.2f} to {grouped.iloc[-1]:.2f} over the selected period."

def generate_weekly_summary():
    logs = filter_logs_by_days(load_logs(), 7)
    summary = get_summary(logs)
    chart_path = plot_emotion_graph(logs, "data/weekly_emotion_chart.png")
    return summary, chart_path

def generate_monthly_summary():
    logs = filter_logs_by_days(load_logs(), 30)
    summary = get_summary(logs)
    chart_path = plot_emotion_graph(logs, "data/monthly_emotion_chart.png")
    return summary, chart_path

def generate_overall_summary():
    logs = load_logs()
    summary = get_summary(logs)
    chart_path = plot_emotion_graph(logs, "data/overall_emotion_chart.png")
    user_history = '\n'.join([log["user_input"] for log in logs if log.get("user_input")])
    if user_history:
        prompt = f"""
You are a clinical psychology assistant AI. Given the following therapy chat history, analyze and summarize the likely root causes and triggers of the user's mental health issues. Make your analysis personalized and reference patterns or repeated themes. The more data provided, the more detailed and accurate your analysis should be. If possible, suggest what might be underlying issues, but always include a disclaimer that this is not a medical diagnosis.\n\nTherapy chat history:\n{user_history}\n\nRespond with:\nRoot Causes and Triggers: (A detailed, empathetic, and personalized analysis based on the user's history. Reference patterns, repeated themes, and possible underlying issues. End with a disclaimer that this is not a medical diagnosis.)\n"""
        try:
            response = llm.generate([prompt.strip()])
            analysis = response.generations[0][0].text.strip()
        except Exception:
            analysis = "(Could not generate personalized analysis.)"
    else:
        analysis = "Not enough data for a personalized analysis."
    full_summary = summary + "\n\n" + analysis
    return full_summary, chart_path

def generate_advanced_dashboard(period_days=30, period_label='Monthly'):
    logs = filter_logs_by_days(load_logs(), period_days)
    summary = get_summary(logs)
    emotion_chart = plot_emotion_graph(logs, f"data/{period_label.lower()}_emotion_chart.png")
    sentiment_chart = plot_sentiment_over_time(logs, f"data/{period_label.lower()}_sentiment_chart.png", window=3, period='day')
    trend_summary = summarize_trends(logs, period='day')
    return summary, emotion_chart, sentiment_chart, trend_summary
