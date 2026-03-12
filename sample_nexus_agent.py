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
        except:
            pass
    
    def log_agent_stop(self, agent_name):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/agent/stop", 
                        params={"agent_name": agent_name}, timeout=1)
        except:
            pass
    
    def log_task_start(self, agent_name, task_id, task_name):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/task/start", 
                        params={"agent_name": agent_name, "task_id": task_id, "task_name": task_name}, timeout=1)
        except:
            pass
    
    def log_task_complete(self, agent_name, task_id, success=True, error=None):
        try:
            requests.post(f"{self.dashboard_url}/api/hooks/task/complete", 
                        params={"agent_name": agent_name, "task_id": task_id, 
                               "success": success, "error": error if error else ""}, timeout=1)
        except:
            pass

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
            # Simulate work
            time.sleep(random.uniform(1, 3))
            
            # 90% success rate
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
    # Create agent
    agent = SampleNexusAIAgent("SampleAgent")
    
    # Run some tasks
    try:
        for i in range(5):
            agent.execute_task(f"Task-{i+1}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        agent.shutdown()
