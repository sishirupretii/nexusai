from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import threading

router = APIRouter(prefix="/api", tags=["dashboard"])

# In-memory storage for agent logs
_agent_logs = []
_task_logs = []
_log_lock = threading.Lock()

class NexusAILogger:
    """Hook for logging agent activities"""
    
    @staticmethod
    def log_agent_start(agent_name: str):
        """Log when an agent starts"""
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
        """Log when an agent stops"""
        with _log_lock:
            for log in _agent_logs:
                if log["agent_name"] == agent_name and log["status"] == "active":
                    log["status"] = "inactive"
                    log["end_time"] = datetime.now().isoformat()
                    break
    
    @staticmethod
    def log_task_start(agent_name: str, task_id: str, task_name: str):
        """Log when a task starts"""
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
        """Log when a task completes"""
        with _log_lock:
            for log in _task_logs:
                if log["task_id"] == task_id and log["status"] == "running":
                    log["status"] = "completed"
                    log["end_time"] = datetime.now().isoformat()
                    log["success"] = success
                    log["error"] = error
                    
                    # Update agent stats
                    for agent in _agent_logs:
                        if agent["agent_name"] == agent_name:
                            agent["tasks_completed"] += 1
                            if success:
                                agent["success_count"] += 1
                            else:
                                agent["failure_count"] += 1
                            break
                    break

# Create a global logger instance
logger = NexusAILogger()

@router.get("/agents")
async def get_agents() -> List[Dict[str, Any]]:
    """Get all agents and their status"""
    with _log_lock:
        agents = []
        for agent in _agent_logs:
            # Calculate success rate
            total = agent["success_count"] + agent["failure_count"]
            success_rate = (agent["success_count"] / total * 100) if total > 0 else 0
            
            agents.append({
                "name": agent["agent_name"],
                "status": agent["status"],
                "tasks_completed": agent["tasks_completed"],
                "success_rate": round(success_rate, 2),
                "success_count": agent["success_count"],
                "failure_count": agent["failure_count"],
                "last_seen": agent.get("timestamp", "")
            })
        return agents

@router.get("/tasks")
async def get_tasks(limit: int = 50) -> List[Dict[str, Any]]:
    """Get recent tasks"""
    with _log_lock:
        return sorted(_task_logs, key=lambda x: x["start_time"], reverse=True)[:limit]

@router.get("/logs")
async def get_logs(limit: int = 100) -> List[Dict[str, Any]]:
    """Get recent activity logs"""
    with _log_lock:
        logs = []
        
        # Combine agent and task logs with timestamps
        for agent in _agent_logs:
            logs.append({
                "timestamp": agent["timestamp"],
                "type": "agent",
                "message": f"Agent '{agent['agent_name']}' started",
                "status": agent["status"]
            })
        
        for task in _task_logs:
            if task["status"] == "completed":
                status = "✓" if task["success"] else "✗"
                message = f"Task '{task['task_name']}' {status}"
                if task["error"]:
                    message += f" - {task['error']}"
            else:
                message = f"Task '{task['task_name']}' started"
            
            logs.append({
                "timestamp": task["start_time"],
                "type": "task",
                "message": message,
                "status": "success" if task.get("success") else "failure" if task.get("success") is False else "running"
            })
        
        # Sort by timestamp and return latest first
        return sorted(logs, key=lambda x: x["timestamp"], reverse=True)[:limit]

@router.post("/hooks/agent/start")
async def hook_agent_start(agent_name: str):
    """Hook for agents to call when starting"""
    logger.log_agent_start(agent_name)
    return {"status": "logged"}

@router.post("/hooks/agent/stop")
async def hook_agent_stop(agent_name: str):
    """Hook for agents to call when stopping"""
    logger.log_agent_stop(agent_name)
    return {"status": "logged"}

@router.post("/hooks/task/start")
async def hook_task_start(agent_name: str, task_id: str, task_name: str):
    """Hook for agents to call when starting a task"""
    logger.log_task_start(agent_name, task_id, task_name)
    return {"status": "logged"}

@router.post("/hooks/task/complete")
async def hook_task_complete(agent_name: str, task_id: str, success: bool = True, error: str = None):
    """Hook for agents to call when completing a task"""
    logger.log_task_complete(agent_name, task_id, success, error)
    return {"status": "logged"}
