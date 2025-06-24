import os
import json
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt

LOG_FILE = "data/emotion_log.json"

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
    return summary, chart_path
