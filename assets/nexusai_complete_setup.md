NexusAI - Complete System Documentation
markdown
<div align="center">

<img src="nexusai_logo.png" alt="NexusAI" width="600">

<br/>

# Just talk to your agent — it learns and *EVOLVES*.

<p>
  <a href="https://github.com/yourusername/NexusAI"><img src="https://img.shields.io/badge/github-NexusAI-181717?style=flat&labelColor=555&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat&labelColor=555" alt="License MIT"></a>
  <img src="https://img.shields.io/badge/🔌_Virtuals_Protocol_Ready-purple?style=flat&labelColor=555" alt="Virtuals Protocol Ready" />
  <img src="https://img.shields.io/badge/⚡_Async_API-yellow?style=flat&labelColor=555" alt="Async API" />
  <img src="https://img.shields.io/badge/☁️_No_GPU_Required-blue?style=flat&labelColor=555" alt="No GPU Required" />
  <img src="https://img.shields.io/badge/📊_Real--time_Dashboard-orange?style=flat&labelColor=555" alt="Real-time Dashboard" />
  <img src="https://img.shields.io/badge/🚀_One--Click_Deploy-green?style=flat&labelColor=555" alt="One-Click Deploy" />
</p>

</div>

---

# NexusAI - AI Agent System for Virtuals Protocol

NexusAI is a powerful AI agent system rebranded from MetaClaw, now fully compatible with the Virtuals Protocol ecosystem. It provides a lightweight API layer that exposes AI agents as callable endpoints, complete with a real-time monitoring dashboard.

## 📋 Table of Contents
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Dashboard](#-dashboard)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Virtuals Protocol Integration](#-virtuals-protocol-integration)
- [Adding Custom Agents](#-adding-custom-agents)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features

### Virtuals Protocol Compatible
Ready-to-use API endpoints for agent integration. Your agents can be called by any Virtuals-compatible system.

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/agent/research` | Research agent - get information on topics |
| `POST /api/v1/agent/code` | Code agent - generate programming solutions |
| `POST /api/v1/agent/analyze` | Analysis agent - analyze data and patterns |
| `GET /api/v1/agents` | List all available agents |

### Real-time Dashboard
Monitor all agent activity in real-time:
- **Active Agents** - See which agents are running
- **Task Statistics** - Completed tasks, success rates
- **Activity Logs** - Timestamped agent actions
- **Auto-refresh** - Updates every 5 seconds

### One-Click Deployment
```bash
python nexusai_api.py        # Start API server (port 8001)
python standalone_dashboard.py  # Start dashboard (port 8000)
Additional Features
✅ CORS Enabled - Cross-origin support for web applications

✅ Lightweight - Minimal dependencies, easy to deploy

✅ Extensible - Easy to add new agent types

✅ No GPU Required - Works with any OpenAI-compatible LLM

✅ Async by Design - Serving and processing are fully decoupled

✅ Mock Mode - Built-in responses for testing

✅ Production Mode - Connect to real MetaClaw agents

📊 System Architecture
text
┌─────────────────┐     ┌─────────────────┐
│  Dashboard      │     │  API Server     │
│  (Port 8000)    │     │  (Port 8001)    │
│  Monitoring UI  │     │  Virtuals Compat│
└────────┬────────┘     └────────┬────────┘
         │                       │
         └──────────┬────────────┘
                    ▼
        ┌───────────────────────┐
        │    MetaClaw Core       │
        │    (Unmodified)        │
        └───────────────────────┘
🚀 Quick Start
1. Install Dependencies
bash
pip install fastapi uvicorn pydantic requests
2. Start the API Server
bash
python nexusai_api.py
The API server will start on http://localhost:8001

3. Start the Dashboard (Optional)
bash
python standalone_dashboard.py
The dashboard will be available at http://localhost:8000

4. Test Your Agents
bash
# Test research agent
curl -X POST "http://localhost:8001/api/v1/agent/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is blockchain?"}'

# Test code agent
curl -X POST "http://localhost:8001/api/v1/agent/code" \
  -H "Content-Type: application/json" \
  -d '{"query": "Write a Python function"}'

# Test analyze agent
curl -X POST "http://localhost:8001/api/v1/agent/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze this data"}'

# List all agents
curl http://localhost:8001/api/v1/agents

# API info
curl http://localhost:8001/
📊 API Reference
Base URL
text
http://localhost:8001/api/v1
Endpoints
POST /agent/research
Research agent - get information on any topic.

Request:

json
{
  "query": "What is quantum computing?",
  "context": {},
  "session_id": "optional-session-id"
}
Response:

json
{
  "agent": "research",
  "result": "Research findings for: What is quantum computing?",
  "session_id": "generated-uuid",
  "error": null
}
POST /agent/code
Code generation agent - create programming solutions.

Request:

json
{
  "query": "Write a REST API in Python",
  "context": {},
  "session_id": "optional-session-id"
}
Response:

json
{
  "agent": "code",
  "result": "Generated code solution for: Write a REST API in Python",
  "session_id": "generated-uuid",
  "error": null
}
POST /agent/analyze
Analysis agent - analyze data and find patterns.

Request:

json
{
  "query": "Find trends in this sales data",
  "context": {},
  "session_id": "optional-session-id"
}
Response:

json
{
  "agent": "analyze",
  "result": "Analysis results for: Find trends in this sales data",
  "session_id": "generated-uuid",
  "error": null
}
GET /agents
List all available agents.

Response:

json
{
  "agents": ["research", "code", "analyze"],
  "total": 3
}
GET /
API information and endpoints.

Response:

json
{
  "name": "NexusAI Agent API",
  "version": "1.0.0",
  "compatible_with": "Virtuals Protocol",
  "endpoints": [
    "POST /api/v1/agent/research",
    "POST /api/v1/agent/code",
    "POST /api/v1/agent/analyze",
    "GET /api/v1/agents"
  ]
}
GET /health
Health check endpoint.

Response:

json
{
  "status": "healthy",
  "service": "NexusAI API"
}
📊 Dashboard
The dashboard at http://localhost:8000 provides:

Features:
Active Agents - Real-time view of running agents

Task Statistics - Completed tasks, success rates

Activity Logs - Timestamped agent actions

Auto-refresh - Updates every 5 seconds

Dashboard Components:
text
┌─────────────────────────────────────┐
│  Header: NexusAI Agent Dashboard    │
├─────────────────────────────────────┤
│  Stats Cards:                       │
│  • Active Agents    • Running Tasks │
│  • Tasks Completed  • Failed Tasks  │
├─────────────────────────────────────┤
│  Active Agents Table                │
│  ┌──────────┬──────┬──────┬──────┐ │
│  │ Name     │Status│Tasks │Rate  │ │
│  ├──────────┼──────┼──────┼──────┤ │
│  │ Agent1   │active│ 42   │ 95%  │ │
│  └──────────┴──────┴──────┴──────┘ │
├─────────────────────────────────────┤
│  Recent Tasks & Activity Logs       │
└─────────────────────────────────────┘
🔧 Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Full Installation
bash
# Clone the repository
git clone https://github.com/yourusername/NexusAI.git
cd NexusAI

# Install dependencies
pip install fastapi uvicorn pydantic requests

# For development with extra features
pip install -e .              # Basic installation
pip install -e ".[rl]"        # With RL support
pip install -e ".[evolve]"    # With skill evolution
⚙️ Configuration
API Server Configuration
Edit nexusai_api.py to modify:

python
# Change port
port = 8001  # Modify this value

# Add custom agents
def run_agent(agent_type: str, query: str, context: dict = None):
    if agent_type == "custom":
        # Your custom agent logic
        return f"Custom result: {query}"
    # ... existing agents
Dashboard Configuration
Edit standalone_dashboard.py to modify:

python
# Change port
PORT = 8000  # Modify this value

# Change refresh interval (milliseconds)
# In the HTML/JavaScript section:
refreshInterval = setInterval(fetchData, 5000)  # 5000ms = 5 seconds
Environment Variables (Optional)
bash
export NEXUSAI_API_PORT=8001
export NEXUSAI_DASHBOARD_PORT=8000
export NEXUSAI_API_HOST=0.0.0.0
🔌 Virtuals Protocol Integration
NexusAI is fully compatible with Virtuals Protocol. Your agents can be called by any Virtuals-compatible system:

Python Example
python
import requests

# Call research agent
response = requests.post(
    "http://your-nexusai-server:8001/api/v1/agent/research",
    json={"query": "Analyze this market data"}
)
print(response.json()["result"])

# Call code agent
response = requests.post(
    "http://your-nexusai-server:8001/api/v1/agent/code",
    json={"query": "Generate a smart contract"}
)
print(response.json()["result"])
JavaScript Example
javascript
// Call analyze agent
fetch('http://localhost:8001/api/v1/agent/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'Find patterns in this dataset'})
})
.then(res => res.json())
.then(data => console.log(data.result));

// List available agents
fetch('http://localhost:8001/api/v1/agents')
  .then(res => res.json())
  .then(data => console.log(data.agents));
Virtuals Protocol Compatibility Matrix
Feature	Status
REST API	✅
JSON Format	✅
Session Management	✅
Error Handling	✅
CORS Support	✅
Async Processing	✅
🎯 Adding Custom Agents
Method 1: Modify run_agent function
Edit nexusai_api.py:

python
def run_agent(agent_type: str, query: str, context: dict = None):
    """Execute agents - add your custom agents here"""
    
    if agent_type == "research":
        # Your research agent logic
        return f"Research findings for: {query}"
        
    elif agent_type == "code":
        # Your code agent logic
        return f"Generated code for: {query}"
        
    elif agent_type == "analyze":
        # Your analyze agent logic
        return f"Analysis results for: {query}"
        
    elif agent_type == "custom":
        # ADD YOUR CUSTOM AGENT HERE
        # Example: from my_agents import CustomAgent
        # agent = CustomAgent()
        # return agent.process(query)
        return f"Custom agent result for: {query}"
        
    else:
        return f"Unknown agent type: {agent_type}"
Method 2: Create a new endpoint
Add to nexusai_api.py:

python
@app.post("/api/v1/agent/custom", response_model=AgentResponse)
async def custom_agent(request: AgentRequest):
    """Custom agent endpoint"""
    session_id = request.session_id or str(uuid.uuid4())
    
    # Your custom logic here
    result = f"Custom processing: {request.query}"
    
    return AgentResponse(
        agent="custom",
        result=result,
        session_id=session_id
    )
Method 3: Import from external modules
python
# At the top of nexusai_api.py
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your custom agents
from my_agents import ResearchAgent, CodeAgent, CustomAgent

def run_agent(agent_type: str, query: str, context: dict = None):
    if agent_type == "research":
        agent = ResearchAgent()
        return agent.process(query)
    elif agent_type == "custom":
        agent = CustomAgent()
        return agent.execute(query)
📁 Project Structure
text
NexusAI/
├── nexusai/                      # Main package
│   ├── __init__.py               # Package initializer
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── server.py             # API server
│   └── dashboard/                 # Dashboard
│       ├── __init__.py
│       ├── dashboard_server.py    # Dashboard server
│       ├── routes.py              # Dashboard routes
│       └── ui.html                # Dashboard HTML
├── nexusai_api.py                 # Standalone API server
├── standalone_api.py              # Production API server
├── standalone_dashboard.py        # Dashboard server
├── sample_nexus_agent.py          # Sample agent
├── test_integration.py            # Integration tests
├── requirements.txt               # Dependencies
├── LICENSE                        # MIT License
└── README.md                      # This file
🧪 Testing
Run Sample Agent
bash
python sample_nexus_agent.py
Expected output:

text
Initializing agent: SampleAgent
Starting task: Task-1 (ID: 550e8400-e29b-41d4-a716-446655440000)
✓ Task 'Task-1' completed successfully
Starting task: Task-2 (ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8)
✓ Task 'Task-2' completed successfully
...
Shutting down agent: SampleAgent
Run Integration Tests
bash
python test_integration.py
Manual API Testing
bash
# Test all endpoints
curl http://localhost:8001/
curl http://localhost:8001/health
curl http://localhost:8001/api/v1/agents

# Test with different queries
curl -X POST "http://localhost:8001/api/v1/agent/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain neural networks"}'

curl -X POST "http://localhost:8001/api/v1/agent/code" \
  -H "Content-Type: application/json" \
  -d '{"query": "Create a React component"}'

curl -X POST "http://localhost:8001/api/v1/agent/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze customer feedback"}'
Load Testing
bash
# Install load testing tool
pip install locust

# Create locustfile.py
echo "
from locust import HttpUser, task, between

class NexusAIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_research(self):
        self.client.post("/api/v1/agent/research", 
                        json={"query": "test query"})
" > locustfile.py

# Run load test
locust -f locustfile.py --host=http://localhost:8001
🐛 Troubleshooting
Common Issues and Solutions
Port Already in Use
bash
# Find process using the port
netstat -ano | findstr :8001
# Example output: TCP 0.0.0.0:8001 0.0.0.0:0 LISTENING 12345

# Kill the process (replace 12345 with actual PID)
taskkill /PID 12345 /F

# Or kill all Python processes
taskkill /F /IM python.exe
Import Errors
bash
# Reinstall dependencies
pip uninstall fastapi uvicorn pydantic requests -y
pip install fastapi uvicorn pydantic requests

# Check Python path
python -c "import sys; print(sys.path)"
Module Not Found
bash
# Install missing modules
pip install fastapi uvicorn pydantic requests

# If using virtual environment, activate it first
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
Dashboard Not Showing Data
bash
# Ensure both servers are running
# Terminal 1
python nexusai_api.py

# Terminal 2
python standalone_dashboard.py

# Check if ports are correct
curl http://localhost:8001/health
curl http://localhost:8000/
CORS Errors
If you get CORS errors in browser:

python
# In nexusai_api.py, ensure CORS is properly configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Slow Response Times
bash
# Check system resources
tasklist | findstr python

# Monitor API performance
# Add logging to nexusai_api.py
import time

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
🤝 Contributing
How to Contribute
Fork the Repository

bash
git clone https://github.com/yourusername/NexusAI.git
cd NexusAI
Create a Feature Branch

bash
git checkout -b feature/amazing-feature
Make Your Changes

Follow the existing code style

Add comments for complex logic

Update documentation if needed

Test Your Changes

bash
python nexusai_api.py
python standalone_dashboard.py
# Test all endpoints
Commit Your Changes

bash
git add .
git commit -m "Add amazing feature"
Push to Your Fork

bash
git push origin feature/amazing-feature
Open a Pull Request

Describe your changes

Reference any related issues

Wait for review

Development Guidelines
Code Style: Follow PEP 8

Documentation: Update README if needed

Testing: Add tests for new features

Commits: Use clear commit messages

Reporting Issues
When reporting issues, please include:

Steps to reproduce

Expected behavior

Actual behavior

Screenshots (if applicable)

Environment details (OS, Python version)

