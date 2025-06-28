// Fetch and display monthly dashboard data
function loadMonthlyDashboard() {
    fetch('/summary?type=monthly')
        .then(res => res.json())
        .then(data => {
            document.getElementById('summary-output').textContent = data.summary || '';
            if (data.img) {
                document.getElementById('emotion-chart').src = data.img;
                document.getElementById('emotion-chart').style.display = '';
            } else {
                document.getElementById('emotion-chart').style.display = 'none';
            }
        });
    // Fetch advanced dashboard (sentiment chart, trend summary)
    fetch('/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: 'trend_summary', days: 30})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('trend-summary').textContent = data.answer || '';
    });
    // Sentiment chart (assuming /summary returns only emotion chart)
    fetch('/static/data/monthly_sentiment_chart.png')
        .then(res => {
            if (res.ok) {
                document.getElementById('sentiment-chart').src = '/static/data/monthly_sentiment_chart.png';
                document.getElementById('sentiment-chart').style.display = '';
            } else {
                document.getElementById('sentiment-chart').style.display = 'none';
            }
        });
}

window.onload = function() {
    loadMonthlyDashboard();
    // Q&A logic
    const suggested = document.getElementById('suggested-questions');
    const qaInput = document.getElementById('qa-input');
    const qaSubmit = document.getElementById('qa-submit');
    const qaAnswer = document.getElementById('qa-answer');
    suggested.onchange = function() {
        if (suggested.value) qaInput.value = suggested.value;
    };
    qaSubmit.onclick = function() {
        const question = qaInput.value.trim();
        if (!question) return;
        qaAnswer.textContent = 'Analyzing...';
        fetch('/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question, days: 30})
        })
        .then(res => res.json())
        .then(data => {
            qaAnswer.textContent = data.answer || 'No answer.';
        });
    };
}; 