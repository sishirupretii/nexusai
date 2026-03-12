# NexusAI Dashboard Integration Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NexusAI Dashboard - MetaClaw Integration" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Main menu
Write-Host "Select integration option:" -ForegroundColor Yellow
Write-Host "1. Auto-detect and add hooks to all agent files"
Write-Host "2. Manually specify agent files to modify"
Write-Host "3. Create sample agent with hooks"
Write-Host "4. Just show the code to add manually"
$choice = Read-Host "`nEnter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`nSearching for agent files..." -ForegroundColor Green
        $agentFiles = Get-ChildItem -Path "." -Recurse -Include "*.py" | Where-Object { 
            $_.Name -match "agent|task|worker" -or 
            (Get-Content $_.FullName -Raw) -match "class.*Agent" 
        }
        
        if ($agentFiles.Count -eq 0) {
            Write-Host "No agent files found automatically." -ForegroundColor Red
        } else {
            Write-Host "Found $($agentFiles.Count) potential agent files:" -ForegroundColor Green
            foreach ($file in $agentFiles) {
                Write-Host "  - $($file.FullName)" -ForegroundColor White
            }
            
            $confirm = Read-Host "`nThis will modify these files. Continue? (y/n)"
            if ($confirm -eq 'y') {
                Write-Host "`nAuto-modification selected. Please check the files manually and add the hooks." -ForegroundColor Yellow
                Write-Host "See option 4 for the code to add." -ForegroundColor Yellow
            }
        }
    }
    
    "2" {
        Write-Host "`nEnter path to Python file (or 'done' to finish):" -ForegroundColor Yellow
        $files = @()
        while ($true) {
            $path = Read-Host "File path"
            if ($path -eq 'done') { break }
            if (Test-Path $path) {
                $files += $path
                Write-Host "  ✓ Added: $path" -ForegroundColor Green
            } else {
                Write-Host "  ✗ File not found: $path" -ForegroundColor Red
            }
        }
        
        Write-Host "`nSelected files:" -ForegroundColor Cyan
        foreach ($file in $files) {
            Write-Host "  - $file" -ForegroundColor White
        }
        Write-Host "`nPlease add the hooks manually (see option 4 for the code)." -ForegroundColor Yellow
    }
    
    "3" {
        $samplePath = Read-Host "Enter path for sample agent file (e.g., ./sample_agent.py)"
        
        @"
import uuid
import time
import random
import requests

# NexusAI Dashboard Logger
class NexusAILogger:
    def __init__(self, dashboard_url="http://localhost:8000"):
        self.dashboard_url = dashboard_url
    
    def log_agent_start(self, agent_name):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/agent/start", 
                        params={"agent_name": agent_name}, timeout=1)
        except: pass
    
    def log_agent_stop(self, agent_name):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/agent/stop", 
                        params={"agent_name": agent_name}, timeout=1)
        except: pass
    
    def log_task_start(self, agent_name, task_id, task_name):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/task/start", 
                        params={"agent_name": agent_name, "task_id": task_id, "task_name": task_name}, timeout=1)
        except: pass
    
    def log_task_complete(self, agent_name, task_id, success=True, error=None):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/task/complete", 
                        params={"agent_name": agent_name, "task_id": task_id, 
                               "success": success, "error": error if error else ""}, timeout=1)
        except: pass

logger = NexusAILogger()

class SampleNexusAIAgent:
    def __init__(self, name):
        self.name = name
        print(f"Initializing agent: {name}")
        logger.log_agent_start(name)
    
    def execute_task(self, task_name):
        task_id = str(uuid.uuid4())
        logger.log_task_start(self.name, task_id, task_name)
        print(f"Starting task: {task_name} (ID: {task_id})")
        
        try:
            time.sleep(random.uniform(1, 3))
            
            if random.random() < 0.9:
                result = f"Task '{task_name}' completed successfully"
                print(f"✓ {result}")
                logger.log_task_complete(self.name, task_id, success=True)
                return result
            else:
                raise Exception("Random task failure")
                
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Task failed: {error_msg}")
            logger.log_task_complete(self.name, task_id, success=False, error=error_msg)
            raise
    
    def shutdown(self):
        print(f"Shutting down agent: {self.name}")
        logger.log_agent_stop(self.name)

if __name__ == "__main__":
    agent = SampleNexusAIAgent("SampleAgent")
    try:
        for i in range(5):
            agent.execute_task(f"Task-{i+1}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        agent.shutdown()
"@ | Out-File -FilePath $samplePath -Encoding utf8
        
        Write-Host "`n✅ Sample agent created at: $samplePath" -ForegroundColor Green
        Write-Host "Run it with: python $samplePath" -ForegroundColor Yellow
        Write-Host "Make sure the dashboard is running first: python standalone_dashboard.py" -ForegroundColor Yellow
    }
    
    "4" {
        Write-Host "`n📋 Copy this code to add to your agent files:" -ForegroundColor Cyan
        Write-Host "`n" + ("="*60) -ForegroundColor Gray
        Write-Host @"

# Add these imports at the top:
import uuid
import requests

# Add this logger class:
class NexusAILogger:
    def __init__(self, dashboard_url='http://localhost:8000'):
        self.dashboard_url = dashboard_url
    
    def log_agent_start(self, agent_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/agent/start', 
                        params={'agent_name': agent_name}, timeout=1)
        except: pass
    
    def log_agent_stop(self, agent_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/agent/stop', 
                        params={'agent_name': agent_name}, timeout=1)
        except: pass
    
    def log_task_start(self, agent_name, task_id, task_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/task/start', 
                        params={'agent_name': agent_name,
                               'task_id': task_id,
                               'task_name': task_name}, timeout=1)
        except: pass
    
    def log_task_complete(self, agent_name, task_id, success=True, error=None):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/task/complete', 
                        params={'agent_name': agent_name,
                               'task_id': task_id,
                               'success': success,
                               'error': error if error else ''}, timeout=1)
        except: pass

logger = NexusAILogger()

# In your agent class:
class YourAgent:
    def __init__(self, name):
        self.name = name
        logger.log_agent_start(name)  # Add this
    
    def run_task(self, task_name):
        task_id = str(uuid.uuid4())
        logger.log_task_start(self.name, task_id, task_name)  # Add this
        
        try:
            # Your task logic
            result = self._do_work()
            logger.log_task_complete(self.name, task_id, success=True)  # Add this
            return result
        except Exception as e:
            logger.log_task_complete(self.name, task_id, success=False, error=str(e))  # Add this
            raise
    
    def shutdown(self):
        logger.log_agent_stop(self.name)  # Add this
"@ -ForegroundColor White
        Write-Host "="*60 -ForegroundColor Gray
    }
}

Write-Host "`n✅ Done! Make sure the NexusAI Dashboard is running (http://localhost:8000)" -ForegroundColor Green
