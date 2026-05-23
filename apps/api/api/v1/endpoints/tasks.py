from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class TaskResponse(BaseModel):
    task_id: str
    status: str
    agent_id: str
    result: Optional[dict] = None


@router.get("/", response_model=List[TaskResponse])
async def list_tasks():
    """List all tasks."""
    # TODO: Implement task listing
    return []


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task details."""
    # TODO: Implement task retrieval
    return {
        "task_id": task_id,
        "status": "completed",
        "agent_id": "agent-1",
        "result": {},
    }


@router.delete("/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a running task."""
    # TODO: Implement task cancellation
    return {"message": "Task cancelled"}
