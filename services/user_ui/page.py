# --- Frontend HTML (For easy testing) ---

def get_frontend_html():
    # Simple HTML/JS client using WebSockets to interact with the backend
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Search Demo</title>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            #statusLog { border: 1px solid #ccc; padding: 10px; height: 200px; overflow-y: scroll; margin-top: 15px; background: #f9f9f9; }
            .progress-bar-container { width: 100%; background-color: #ddd; border-radius: 5px; margin: 5px 0; }
            .progress-bar { height: 20px; width: 0%; background-color: #4CAF50; text-align: center; line-height: 20px; color: white; border-radius: 5px; }
            .result-item { border-bottom: 1px solid #eee; padding: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Video Search Indexer</h1>
        
        <input type="text" id="videoPath" value="/mock/video1.mp4" placeholder="Mock Video Path">
        <input type="text" id="etalonName" value="etalon_car_1.jpg" placeholder="Mock Etalon Image Name">
        <input type="number" id="threshold" value="0.85" step="0.01" placeholder="Similarity Threshold">
        <button onclick="startSearch()">Start Index & Search</button>
        
        <h2>Task Status</h2>
        <div id="statusLog">Waiting for tasks...</div>
        
        <h2>Results</h2>
        <div id="resultsArea"></div>

        <script>
            const statusLog = document.getElementById('statusLog');
            const resultsArea = document.getElementById('resultsArea');
            let ws;
            let currentTaskId = null;

            function log(message, isResult = false) {
                const entry = document.createElement('div');
                entry.innerHTML = message;
                if (isResult) {
                    entry.style.fontWeight = 'bold';
                    entry.style.color = 'darkgreen';
                }
                statusLog.appendChild(entry);
                statusLog.scrollTop = statusLog.scrollHeight;
            }

            function updateProgressBar(statusData) {
                const taskId = statusData.task_id;
                let statusDiv = document.getElementById('task_' + taskId);
                
                if (!statusDiv) {
                    statusDiv = document.createElement('div');
                    statusDiv.id = 'task_' + taskId;
                    statusDiv.className = 'task-entry';
                    statusDiv.innerHTML = <strong>Task ${taskId}</strong>: <div class="progress-bar-container"><div id="bar_${taskId}" class="progress-bar">0%</div></div>;
                    statusLog.appendChild(statusDiv);
                }

                const bar = document.getElementById('bar_' + taskId);
                bar.style.width = statusData.progress + '%';
                bar.textContent = statusData.progress + '% (' + statusData.status + ')';
                
                if (statusData.progress === 100) {
                    log(✅ Task ${taskId} finished: ${statusData.message}, true);
                    if (statusData.result) {
                        displayResults(statusData.result);
                    }
                }
            }

            function displayResults(results) {
                resultsArea.innerHTML = '';
                if (results.length === 0) {
                    resultsArea.innerHTML = '<p>No similar segments found above the threshold.</p>';
                    return;
                }
                
                resultsArea.innerHTML = <p>Found ${results.length} potential matches:</p>;
                results.forEach(res => {
                    const item = document.createElement('div');
                    item.className = 'result-item';
                    item.innerHTML = 
                        Video: ${res.video_id} | Frame Index: ${res.frame_index} 
                        (Score: ${(res.similarity_score * 100).toFixed(2)}%)
                        <br><em>(In a real app, this would map to a video clip)</em>
                    ;
                    resultsArea.appendChild(item);
                });
            }

            function startSearch() {
                const videoPath = document.getElementById('videoPath').value;
                const etalonName = document.getElementById('etalonName').value;
                const threshold = document.getElementById('threshold').value;
                
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    log("Error: WebSocket not connected. Reconnecting...");
                    connectWebSocket();
                    return;
                }
                
                log(--- Starting Job for ${videoPath} with threshold ${threshold} ---);
                resultsArea.innerHTML = '';
                
                ws.send(JSON.stringify({
                    action: "START_INDEXING",
                    payload: {
                        video_path: videoPath,
                        etalon_filename: etalonName,
                        threshold: threshold
                    }
                }));
            }

            function connectWebSocket() {
                ws = new WebSocket("ws://localhost:8000/ws");
                
                ws.onopen = () => {
                    log("Connection established.");
                    // Immediately request status updates for any existing tasks
                    if (currentTaskId) {
                         ws.send(JSON.stringify({ action: "GET_STATUS", payload: { task_id: currentTaskId } }));
                    }
                };

                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === "TASK_STARTED") {
                        currentTaskId = data.task_id;
                        log(Task initialized: ${currentTaskId}. Waiting for updates...);
                    } 
                    
                    if (data.type === "STATUS_UPDATE") {
                        const status = data.data;
                        if (status) {
                            updateProgressBar(status);
                        }
                    }
                    
                    if (data.type === "ERROR") {
                        log(ERROR: ${data.message}, true);
                    }
                };

                ws.onclose = () => {
                    log("Connection closed. Attempting to reconnect in 3 seconds...");
                    currentTaskId = null;
                    setTimeout(connectWebSocket, 3000);
                };
            }

            window.onload = () => {
                connectWebSocket();
                
                // Polling mechanism (since the broadcaster doesn't push to unconnected clients easily)
                setInterval(() => {
                    if (ws && ws.readyState === WebSocket.OPEN && currentTaskId) {
                        ws.send(JSON.stringify({ action: "GET_STATUS", payload: { task_id: currentTaskId } }));
                    }
                }, 1500); // Poll status every 1.5 seconds
            };
        </script>
    </body>
    </html>
    """
