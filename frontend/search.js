// Session search functionality
function doSearch() {
    const query = document.getElementById('search-query').value.trim();
    const output = document.getElementById('search-output');
    if (!query) return;
    
    // Show loading with animation
    output.innerHTML = '<div class="loading-spinner">🔍 Searching sessions...</div>';
    
    fetch('/search_sessions', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query})
    })
    .then(res => res.json())
    .then(data => {
        const summaries = data.summaries || {};
        if (Object.keys(summaries).length === 0) {
            output.innerHTML = '<div style="color: #666; text-align: center; padding: 20px;">No matching sessions found.</div>';
            return;
        }
        
        let html = '<div style="margin-bottom: 10px;"><strong>Found ' + Object.keys(summaries).length + ' matching session(s):</strong></div>';
        
        for (const [sessionId, summary] of Object.entries(summaries)) {
            const timestamp = new Date(summary.timestamp).toLocaleString();
            const shortId = sessionId.substring(0, 8);
            
            html += `
                <div class="session-card" onclick="viewSession('${sessionId}')" style="
                    border: 1px solid #b2dfdb; 
                    border-radius: 8px; 
                    padding: 12px; 
                    margin: 8px 0; 
                    cursor: pointer; 
                    background: #f8fafc;
                    transition: background 0.2s;
                " onmouseover="this.style.background='#e8f5e9'" onmouseout="this.style.background='#f8fafc'">
                    <div style="font-weight: 500; color: #388e3c; margin-bottom: 4px;">
                        Session ${shortId} • ${timestamp} • ${summary.message_count} messages
                    </div>
                    <div style="color: #234c2e; font-style: italic;">
                        "${summary.first_message.substring(0, 100)}${summary.first_message.length > 100 ? '...' : ''}"
                    </div>
                    <div style="font-size: 0.9em; color: #666; margin-top: 4px;">
                        Emotion: ${summary.emotion}
                    </div>
                </div>
            `;
        }
        
        output.innerHTML = html;
    })
    .catch(error => {
        console.error('Search error:', error);
        output.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 20px;">Sorry, there was an error performing the search.</div>';
    });
}

document.getElementById('search-submit').onclick = doSearch;

// Ensure Enter key works for search
document.getElementById('search-query').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        doSearch();
    }
});

// Load session summaries for history view
function loadHistory() {
    const output = document.getElementById('history-output');
    output.innerHTML = '<div class="loading-spinner">📜 Loading sessions...</div>';
    
    fetch('/session_summaries')
        .then(res => res.json())
        .then(data => {
            const summaries = data.summaries || {};
            if (Object.keys(summaries).length === 0) {
                output.innerHTML = '<div style="color: #666; text-align: center; padding: 20px;">No therapy sessions found.</div>';
                return;
            }
            
            // Sort by timestamp (newest first)
            const sortedSessions = Object.entries(summaries).sort((a, b) => 
                new Date(b[1].timestamp) - new Date(a[1].timestamp)
            );
            
            let html = '<div style="margin-bottom: 10px;"><strong>Total sessions: ' + Object.keys(summaries).length + '</strong></div>';
            
            for (const [sessionId, summary] of sortedSessions) {
                const timestamp = new Date(summary.timestamp).toLocaleString();
                const shortId = sessionId.substring(0, 8);
                
                html += `
                    <div class="session-card" onclick="viewSession('${sessionId}')" style="
                        border: 1px solid #b2dfdb; 
                        border-radius: 8px; 
                        padding: 12px; 
                        margin: 8px 0; 
                        cursor: pointer; 
                        background: #f8fafc;
                        transition: background 0.2s;
                    " onmouseover="this.style.background='#e8f5e9'" onmouseout="this.style.background='#f8fafc'">
                        <div style="font-weight: 500; color: #388e3c; margin-bottom: 4px;">
                            Session ${shortId} • ${timestamp} • ${summary.message_count} messages
                        </div>
                        <div style="color: #234c2e; font-style: italic;">
                            "${summary.first_message.substring(0, 100)}${summary.first_message.length > 100 ? '...' : ''}"
                        </div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 4px;">
                            Emotion: ${summary.emotion}
                        </div>
                    </div>
                `;
            }
            
            output.innerHTML = html;
        })
        .catch(error => {
            console.error('History error:', error);
            output.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 20px;">Sorry, there was an error loading the sessions.</div>';
        });
}

// View full session conversation
function viewSession(sessionId) {
    const modal = document.getElementById('session-modal');
    const title = document.getElementById('session-title');
    const conversation = document.getElementById('session-conversation');
    
    title.textContent = `Session ${sessionId.substring(0, 8)} - Full Conversation`;
    conversation.innerHTML = '<div class="loading-spinner">📖 Loading conversation...</div>';
    modal.classList.remove('hidden');
    
    fetch(`/session/${sessionId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                conversation.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 20px;">Session not found.</div>';
                return;
            }
            
            let html = '';
            for (const message of data.conversation) {
                const timestamp = new Date(message.timestamp).toLocaleString();
                const isUser = message.type === 'user';
                
                html += `
                    <div style="
                        margin: 12px 0; 
                        padding: 12px; 
                        border-radius: 8px; 
                        background: ${isUser ? '#e8f5e9' : '#f1f8e9'};
                        border-left: 4px solid ${isUser ? '#388e3c' : '#81c784'};
                    ">
                        <div style="
                            font-weight: 500; 
                            color: ${isUser ? '#388e3c' : '#666'}; 
                            margin-bottom: 4px;
                            font-size: 0.9em;
                        ">
                            ${isUser ? '🧍 You' : '🤖 AI Therapist'} • ${timestamp}
                            ${isUser && message.emotion ? ` • Emotion: ${message.emotion}` : ''}
                        </div>
                        <div style="color: #234c2e; line-height: 1.5;">
                            ${message.message}
                        </div>
                    </div>
                `;
            }
            
            conversation.innerHTML = html || '<div style="color: #666; text-align: center; padding: 20px;">No messages in this session.</div>';
        })
        .catch(error => {
            console.error('Session error:', error);
            conversation.innerHTML = '<div style="color: #d32f2f; text-align: center; padding: 20px;">Sorry, there was an error loading the session.</div>';
        });
}

// Modal controls
document.getElementById('close-session').onclick = function() {
    document.getElementById('session-modal').classList.add('hidden');
};

// Close modal when clicking outside
document.getElementById('session-modal').onclick = function(e) {
    if (e.target === this) {
        this.classList.add('hidden');
    }
};

document.getElementById('history-refresh').onclick = loadHistory;

window.onload = function() {
    loadHistory();
}; 