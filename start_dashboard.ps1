# Start the NexusAI Dashboard
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "   NexusAI Dashboard Launcher" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    python --version 2>&1 | Out-Null
    Write-Host "✓ Python found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host ""
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r nexusai/dashboard/requirements.txt

# Start the dashboard
Write-Host ""
Write-Host "Starting NexusAI Dashboard..." -ForegroundColor Green
Write-Host "Dashboard will be available at: http://localhost:8080" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Run the dashboard
python -m nexusai.dashboard.dashboard_server
