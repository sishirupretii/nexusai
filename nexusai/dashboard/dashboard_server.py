import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import sys
import os

# Add the parent directory to path so we can import routes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import routes
from nexusai.dashboard.routes import router

def create_dashboard_app():
    """Create and configure the FastAPI dashboard application"""
    app = FastAPI(title="NexusAI Agent Dashboard", version="1.0.0")
    
    # Include routes
    app.include_router(router)
    
    # Get the directory containing this file
    current_dir = Path(__file__).parent
    
    # Serve the HTML file
    @app.get("/")
    async def get_dashboard():
        return FileResponse(current_dir / "ui.html")
    
    return app

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║     NexusAI Agent Dashboard           ║
    ║     Running on http://localhost:8080  ║
    ╚═══════════════════════════════════════╝
    """)
    app = create_dashboard_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)
