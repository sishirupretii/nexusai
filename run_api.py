# Run NexusAI API Server
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nexusai.api.server import start_server

if __name__ == "__main__":
    start_server()
