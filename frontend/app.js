// Chat
const userInput = document.getElementById('user-input');
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && this.value.trim()) {
        sendChat(this.value.trim());
        this.value = '';
    }
});

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = '<div class="loading-spinner">🤔 Thinking...</div>';
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    // Loading will be replaced by actual content
}

function sendChat(message) {
    // Show loading for all output areas
    showLoading('reflection-output');
    showLoading('questions-output');
    showLoading('suggestions-output');
    
    fetch('/api_chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_input: message})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('reflection-output').textContent = data.reflection || '';
        document.getElementById('questions-output').textContent = (data.questions || []).join('\n');
        document.getElementById('suggestions-output').textContent = (data.suggestions || []).join('\n');
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('reflection-output').textContent = 'Sorry, there was an error processing your message.';
        document.getElementById('questions-output').textContent = '';
        document.getElementById('suggestions-output').textContent = '';
    });
}
// Clear
const clearBtn = document.getElementById('clear-btn');
clearBtn.onclick = function() {
    fetch('/reset', {method: 'POST'}).then(() => {
        document.getElementById('reflection-output').textContent = '';
        document.getElementById('questions-output').textContent = '';
        document.getElementById('suggestions-output').textContent = '';
        document.getElementById('user-input').value = '';
    });
};

// New Session
const newSessionBtn = document.getElementById('new-session-btn');
newSessionBtn.onclick = function() {
    if (confirm('Start a new therapy session? This will clear the current conversation but keep your history.')) {
        fetch('/new_session', {method: 'POST'})
        .then(res => res.json())
        .then(data => {
            // Clear the current conversation display
            document.getElementById('reflection-output').textContent = '';
            document.getElementById('questions-output').textContent = '';
            document.getElementById('suggestions-output').textContent = '';
            document.getElementById('user-input').value = '';
            
            // Show confirmation
            alert('New session started! Session ID: ' + data.session_id.substring(0, 8));
        })
        .catch(error => {
            console.error('Error starting new session:', error);
            alert('Error starting new session. Please try again.');
        });
    }
};

// Session Info
const sessionInfoBtn = document.getElementById('session-info-btn');
sessionInfoBtn.onclick = function() {
    const modal = document.getElementById('session-info-modal');
    const content = document.getElementById('session-info-content');
    
    modal.classList.remove('hidden');
    content.innerHTML = '<div class="loading-spinner">Loading session info...</div>';
    
    fetch('/current_session')
    .then(res => res.json())
    .then(data => {
        const shortId = data.session_id ? data.session_id.substring(0, 8) : 'None';
        content.innerHTML = `
            <div style="margin-bottom: 15px;">
                <strong>Session ID:</strong> ${shortId}
            </div>
            <div style="margin-bottom: 15px;">
                <strong>Messages in this session:</strong> ${data.message_count}
            </div>
            <div style="margin-bottom: 15px;">
                <strong>Status:</strong> ${data.is_active ? '🟢 Active' : '⚪ Inactive'}
            </div>
            <div style="color: #666; font-size: 0.9em;">
                ${data.is_active ? 'You can continue this session or start a new one.' : 'No active session. Start a new one to begin therapy.'}
            </div>
        `;
    })
    .catch(error => {
        console.error('Error loading session info:', error);
        content.innerHTML = '<div style="color: #d32f2f;">Error loading session information.</div>';
    });
};

// Start new session from modal
document.getElementById('start-new-session-btn').onclick = function() {
    fetch('/new_session', {method: 'POST'})
    .then(res => res.json())
    .then(data => {
        // Clear the current conversation display
        document.getElementById('reflection-output').textContent = '';
        document.getElementById('questions-output').textContent = '';
        document.getElementById('suggestions-output').textContent = '';
        document.getElementById('user-input').value = '';
        
        // Close modal and show confirmation
        document.getElementById('session-info-modal').classList.add('hidden');
        alert('New session started! Session ID: ' + data.session_id.substring(0, 8));
    })
    .catch(error => {
        console.error('Error starting new session:', error);
        alert('Error starting new session. Please try again.');
    });
};

// View session history from modal
document.getElementById('view-session-history-btn').onclick = function() {
    window.open('search.html', '_blank');
};

// Modal controls
document.getElementById('close-session-info').onclick = function() {
    document.getElementById('session-info-modal').classList.add('hidden');
};

// Close modal when clicking outside
document.getElementById('session-info-modal').onclick = function(e) {
    if (e.target === this) {
        this.classList.add('hidden');
    }
};

// Summaries
function showSummary(type) {
    fetch(`/summary?type=${type}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById('summary-content').textContent = data.summary || '';
        if (data.img) {
            document.getElementById('summary-img').src = data.img;
            document.getElementById('summary-img').style.display = '';
        } else {
            document.getElementById('summary-img').style.display = 'none';
        }
        document.getElementById('summary-modal').classList.remove('hidden');
    });
}
document.getElementById('weekly-btn').onclick = () => showSummary('weekly');
document.getElementById('monthly-btn').onclick = () => showSummary('monthly');
document.getElementById('overall-btn').onclick = () => showSummary('overall');
document.getElementById('close-summary').onclick = () => document.getElementById('summary-modal').classList.add('hidden');
// Search
document.getElementById('search-btn').onclick = () => document.getElementById('search-modal').classList.remove('hidden');
document.getElementById('close-search').onclick = () => document.getElementById('search-modal').classList.add('hidden');
document.getElementById('search-submit').onclick = function() {
    const query = document.getElementById('search-query').value.trim();
    if (!query) return;
    fetch('/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('search-output').textContent = data.results || '';
    });
}; 