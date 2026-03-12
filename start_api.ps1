# Start NexusAI Agent API Server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NexusAI Agent API - Virtuals Protocol" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r nexusai/api/requirements.txt

Write-Host ""
Write-Host "Starting NexusAI Agent API Server..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8001" -ForegroundColor Yellow
Write-Host "Compatible with Virtuals Protocol agents" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Run the API server
python nexusai/api/server.py
