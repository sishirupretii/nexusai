import uuid
import time
import requests

# NexusAI Dashboard Logger
class NexusAILogger:
    def __init__(self, dashboard_url='http://localhost:8000'):
        self.dashboard_url = dashboard_url
    
    def log_agent_start(self, agent_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/agent/start', 
                        params={'agent_name': agent_name}, timeout=1)
            print(f'✓ Logged agent start: {agent_name}')
        except Exception as e:
            print(f'⚠ Could not log to dashboard: {e}')
    
    def log_agent_stop(self, agent_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/agent/stop', 
                        params={'agent_name': agent_name}, timeout=1)
            print(f'✓ Logged agent stop: {agent_name}')
        except:
            pass
    
    def log_task_start(self, agent_name, task_id, task_name):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/task/start', 
                        params={'agent_name': agent_name, 'task_id': task_id, 'task_name': task_name}, timeout=1)
            print(f'  ✓ Logged task start: {task_name}')
        except:
            pass
    
    def log_task_complete(self, agent_name, task_id, success=True, error=None):
        try:
            requests.post(f'{self.dashboard_url}/api/hooks/task/complete', 
                        params={'agent_name': agent_name, 'task_id': task_id, 
                               'success': success, 'error': error if error else ''}, timeout=1)
            status = '✓' if success else '✗'
            print(f'  {status} Logged task completion: {task_id}')
        except:
            pass

logger = NexusAILogger()

# Example MetaClaw agent with dashboard integration
class MetaClawAgent:
    def __init__(self, name):
        self.name = name
        print(f'\n🚀 Initializing agent: {name}')
        # Log agent start to dashboard
        logger.log_agent_start(name)
    
    def run_task(self, task_name):
        task_id = str(uuid.uuid4())
        print(f'\n  📋 Running task: {task_name}')
        
        # Log task start
        logger.log_task_start(self.name, task_id, task_name)
        
        try:
            # Simulate work
            time.sleep(2)
            
            # Simulate success (90% of the time)
            import random
            if random.random() < 0.9:
                result = f"Task '{task_name}' completed successfully"
                print(f'  ✅ {result}')
                
                # Log success
                logger.log_task_complete(self.name, task_id, success=True)
                return result
            else:
                raise Exception("Random task failure")
                
        except Exception as e:
            error_msg = str(e)
            print(f'  ❌ Task failed: {error_msg}')
            
            # Log failure
            logger.log_task_complete(self.name, task_id, success=False, error=error_msg)
            raise
    
    def shutdown(self):
        print(f'\n🛑 Shutting down agent: {self.name}')
        logger.log_agent_stop(self.name)

# Test the agent
if __name__ == '__main__':
    print('='*50)
    print('NEXUSAI DASHBOARD INTEGRATION TEST')
    print('='*50)
    print('Make sure the dashboard is running at http://localhost:8000')
    print('='*50)
    
    # Create and test agent
    agent = MetaClawAgent('TestAgent')
    
    try:
        # Run a few tasks
        agent.run_task('Process Data')
        agent.run_task('Train Model')
        agent.run_task('Generate Report')
    except Exception as e:
        print(f'\n⚠ Error: {e}')
    finally:
        agent.shutdown()
    
    print('\n✅ Test complete! Check the dashboard at http://localhost:8000')
