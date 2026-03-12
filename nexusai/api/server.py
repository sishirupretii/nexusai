"""
NexusAI API Server - Virtuals Protocol Integration Layer
"""
import uvicorn
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path so we can import routes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_app():
    """Create FastAPI application for agent API"""
    app = FastAPI(
        title="NexusAI Agent API",
        description="Virtuals Protocol compatible agent endpoints",
        version="1.0.0"
    )
    
    # Enable CORS for Virtuals Protocol
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Import routes using absolute import
    from api.routes import router
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return {
            "name": "NexusAI Agent API",
            "version": "1.0.0",
            "compatible_with": "Virtuals Protocol",
            "endpoints": [
                "POST /api/v1/agent/research",
                "POST /api/v1/agent/code", 
                "POST /api/v1/agent/analyze"
            ]
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "NexusAI API"}
    
    return app

def start_server(host="0.0.0.0", port=8001):
    """Start the NexusAI API server"""
    app = create_app()
    print(f"""
    ╔═══════════════════════════════════════╗
    ║     NexusAI Agent API                 ║
    ║     Virtuals Protocol Compatible      ║
    ║     Running on http://{host}:{port}     ║
    ║     Press Ctrl+C to stop              ║
    ╚═══════════════════════════════════════╝
    """)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
