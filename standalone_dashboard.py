import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from datetime import datetime
import threading
from typing import List, Dict, Any
import uuid

# Create router
router = APIRouter(prefix="/api", tags=["dashboard"])

# In-memory storage
_agent_logs = []
_task_logs = []
_log_lock = threading.Lock()

class NexusAILogger:
    @staticmethod
    def log_agent_start(agent_name: str):
        with _log_lock:
            _agent_logs.append({
                "agent_name": agent_name,
                "status": "active",
                "timestamp": datetime.now().isoformat(),
                "tasks_completed": 0,
                "success_count": 0,
                "failure_count": 0
            })
    
    @staticmethod
    def log_agent_stop(agent_name: str):
        with _log_lock:
            for log in _agent_logs:
                if log["agent_name"] == agent_name and log["status"] == "active":
                    log["status"] = "inactive"
                    break
    
    @staticmethod
    def log_task_start(agent_name: str, task_id: str, task_name: str):
        with _log_lock:
            _task_logs.append({
                "agent_name": agent_name,
                "task_id": task_id,
                "task_name": task_name,
                "status": "running",
                "start_time": datetime.now().isoformat(),
                "end_time": None,
                "success": None,
                "error": None
            })
    
    @staticmethod
    def log_task_complete(agent_name: str, task_id: str, success: bool = True, error: str = None):
        with _log_lock:
            for log in _task_logs:
                if log["task_id"] == task_id and log["status"] == "running":
                    log["status"] = "completed"
                    log["end_time"] = datetime.now().isoformat()
                    log["success"] = success
                    log["error"] = error
                    
                    for agent in _agent_logs:
                        if agent["agent_name"] == agent_name:
                            agent["tasks_completed"] += 1
                            if success:
                                agent["success_count"] += 1
                            else:
                                agent["failure_count"] += 1
                            break
                    break

logger = NexusAILogger()

# Add some sample data for testing
logger.log_agent_start("DataProcessor")
logger.log_agent_start("ModelTrainer")
logger.log_agent_start("NexusCore")
logger.log_task_start("DataProcessor", str(uuid.uuid4()), "Process Dataset")
logger.log_task_start("ModelTrainer", str(uuid.uuid4()), "Train Neural Network")
logger.log_task_start("NexusCore", str(uuid.uuid4()), "Orchestrate Workflow")

# Complete one task as example
sample_task_id = str(uuid.uuid4())
logger.log_task_start("DataProcessor", sample_task_id, "Sample Task")
logger.log_task_complete("DataProcessor", sample_task_id, success=True)

@router.get("/agents")
async def get_agents() -> List[Dict[str, Any]]:
    with _log_lock:
        agents = []
        for agent in _agent_logs:
            total = agent["success_count"] + agent["failure_count"]
            success_rate = (agent["success_count"] / total * 100) if total > 0 else 0
            agents.append({
                "name": agent["agent_name"],
                "status": agent["status"],
                "tasks_completed": agent["tasks_completed"],
                "success_rate": round(success_rate, 2)
            })
        return agents

@router.get("/tasks")
async def get_tasks():
    with _log_lock:
        return sorted(_task_logs, key=lambda x: x["start_time"], reverse=True)[:50]

@router.get("/logs")
async def get_logs():
    with _log_lock:
        logs = []
        for agent in _agent_logs:
            logs.append({
                "timestamp": agent["timestamp"],
                "message": f"Agent '{agent['agent_name']}' started",
                "status": "success"
            })
        for task in _task_logs[:20]:
            if task["status"] == "completed":
                status = "success" if task["success"] else "failure"
                message = f"Task '{task['task_name']}' completed"
            else:
                status = "running"
                message = f"Task '{task['task_name']}' started"
            logs.append({
                "timestamp": task["start_time"],
                "message": message,
                "status": status
            })
        return sorted(logs, key=lambda x: x["timestamp"], reverse=True)[:50]

# Create main app
app = FastAPI(title="NexusAI Agent Dashboard")
app.include_router(router)

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexusAI Agent Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header {
            background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; justify-content: space-between;
            align-items: center;
        }
        h1 { color: #333; font-size: 28px; }
        h1 span { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .port-info {
            background: #f0f0f0; padding: 8px 15px; border-radius: 20px; font-size: 14px; font-weight: bold;
        }
        .stats-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;
        }
        .stat-card {
            background: white; border-radius: 10px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-title { color: #666; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-value { color: #333; font-size: 36px; font-weight: bold; margin-top: 10px; }
        .dashboard-grid {
            display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;
        }
        .card {
            background: white; border-radius: 10px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card h2 { margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; color: #333; }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 12px; background: #f5f5f5; color: #666; font-weight: 600; }
        td { padding: 12px; border-bottom: 1px solid #f0f0f0; }
        .status-badge {
            padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase;
        }
        .status-active { background: #e3f2fd; color: #1976d2; }
        .status-inactive { background: #ffebee; color: #c62828; }
        .status-running { background: #fff3e0; color: #ef6c00; }
        .status-completed { background: #e8f5e8; color: #2e7d32; }
        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;
            font-size: 14px; margin-left: 10px;
        }
        .refresh-btn:hover { opacity: 0.9; }
        .log-container { max-height: 400px; overflow-y: auto; }
        .log-entry {
            padding: 10px; border-bottom: 1px solid #f0f0f0;
            display: flex; align-items: center; gap: 10px;
        }
        .log-time { color: #999; font-size: 12px; min-width: 80px; }
        .log-message { flex: 1; }
        .log-icon { width: 24px; text-align: center; }
        .log-icon.success { color: #4CAF50; }
        .log-icon.failure { color: #f44336; }
        .log-icon.running { color: #FF9800; }
        .last-updated { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 <span>NexusAI</span> Agent Dashboard</h1>
            <div>
                <span class="port-info">Port: 8000</span>
                <span class="last-updated" id="lastUpdated"></span>
                <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
            </div>
        </header>
        
        <div class="stats-grid" id="stats">
            <div class="stat-card"><div class="stat-title">Active Agents</div><div class="stat-value" id="activeAgents">0</div></div>
            <div class="stat-card"><div class="stat-title">Running Tasks</div><div class="stat-value" id="runningTasks">0</div></div>
            <div class="stat-card"><div class="stat-title">Tasks Completed</div><div class="stat-value" id="completedTasks">0</div></div>
            <div class="stat-card"><div class="stat-title">Failed Tasks</div><div class="stat-value" id="failedTasks">0</div></div>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>Active Agents</h2>
                <table id="agentsTable">
                    <thead><tr><th>Agent Name</th><th>Status</th><th>Tasks</th><th>Success Rate</th></tr></thead>
                    <tbody id="agentsBody"><tr><td colspan="4" style="text-align: center;">Loading agents...</td></tr></tbody>
                </table>
            </div>
            <div class="card">
                <h2>Recent Tasks</h2>
                <table id="tasksTable">
                    <thead><tr><th>Task</th><th>Agent</th><th>Status</th></tr></thead>
                    <tbody id="tasksBody"><tr><td colspan="3" style="text-align: center;">Loading tasks...</td></tr></tbody>
                </table>
            </div>
        </div>
        
        <div class="card">
            <h2>Activity Logs</h2>
            <div class="log-container" id="logsContainer">
                <div style="text-align: center; padding: 20px;">Loading logs...</div>
            </div>
        </div>
    </div>
    
    <script>
        async function fetchData() {
            try {
                const [agents, tasks, logs] = await Promise.all([
                    fetch('/api/agents').then(r => r.json()),
                    fetch('/api/tasks').then(r => r.json()),
                    fetch('/api/logs').then(r => r.json())
                ]);
                
                // Update stats
                document.getElementById('activeAgents').textContent = agents.filter(a => a.status === 'active').length;
                document.getElementById('runningTasks').textContent = tasks.filter(t => t.status === 'running').length;
                document.getElementById('completedTasks').textContent = tasks.filter(t => t.status === 'completed' && t.success === true).length;
                document.getElementById('failedTasks').textContent = tasks.filter(t => t.status === 'completed' && t.success === false).length;
                
                // Update agents table
                if (agents.length === 0) {
                    document.getElementById('agentsBody').innerHTML = '<tr><td colspan="4" style="text-align: center;">No agents found</td></tr>';
                } else {
                    document.getElementById('agentsBody').innerHTML = agents.map(a => 
                        <tr>
                            <td></td>
                            <td><span class="status-badge status-"></span></td>
                            <td></td>
                            <td>%</td>
                        </tr>
                    ).join('');
                }
                
                // Update tasks table
                if (tasks.length === 0) {
                    document.getElementById('tasksBody').innerHTML = '<tr><td colspan="3" style="text-align: center;">No tasks found</td></tr>';
                } else {
                    document.getElementById('tasksBody').innerHTML = tasks.slice(0,10).map(t => 
                        <tr>
                            <td></td>
                            <td></td>
                            <td><span class="status-badge status-"></span></td>
                        </tr>
                    ).join('');
                }
                
                // Update logs
                if (logs.length === 0) {
                    document.getElementById('logsContainer').innerHTML = '<div style="text-align: center; padding: 20px;">No logs found</div>';
                } else {
                    document.getElementById('logsContainer').innerHTML = logs.slice(0,20).map(l => {
                        const icon = l.status === 'success' ? '✓' : l.status === 'failure' ? '✗' : '⚡';
                        return 
                            <div class="log-entry">
                                <span class="log-time">[]</span>
                                <span class="log-icon "></span>
                                <span class="log-message"></span>
                            </div>
                        ;
                    }).join('');
                }
                
                // Update last updated time
                document.getElementById('lastUpdated').textContent = Last updated: ;
                
            } catch (e) {
                console.error(e);
                document.getElementById('logsContainer').innerHTML = '<div style="text-align: center; padding: 20px; color: red;">Error loading data. Make sure the server is running.</div>';
            }
        }
        
        function refreshData() { fetchData(); }
        
        // Auto-refresh every 5 seconds
        setInterval(fetchData, 5000);
        
        // Initial load
        fetchData();
    </script>
</body>
</html>
'''

@app.get("/")
async def root():
    return HTMLResponse(content=HTML_CONTENT)

@app.post("/api/hooks/agent/start")
async def hook_agent_start(agent_name: str):
    logger.log_agent_start(agent_name)
    return {"status": "logged"}

@app.post("/api/hooks/agent/stop")
async def hook_agent_stop(agent_name: str):
    logger.log_agent_stop(agent_name)
    return {"status": "logged"}

@app.post("/api/hooks/task/start")
async def hook_task_start(agent_name: str, task_id: str, task_name: str):
    logger.log_task_start(agent_name, task_id, task_name)
    return {"status": "logged"}

@app.post("/api/hooks/task/complete")
async def hook_task_complete(agent_name: str, task_id: str, success: bool = True, error: str = None):
    logger.log_task_complete(agent_name, task_id, success, error)
    return {"status": "logged"}

if __name__ == "__main__":
    PORT = 8000
    print(f"""
    ╔═══════════════════════════════════════╗
    ║     NexusAI Agent Dashboard           ║
    ║     Running on http://localhost:{PORT}  ║
    ║     Press Ctrl+C to stop              ║
    ╚═══════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
