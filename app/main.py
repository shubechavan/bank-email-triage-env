"""
FastAPI server for Bank Support Email Triage OpenEnv.

Endpoints:
  GET  /              → health check
  GET  /tasks         → list all tasks
  POST /reset         → reset environment
  POST /step          → submit action
  GET  /state         → current state
  GET  /emails        → list available emails (for debugging)

Architecture inspired by sanikasalunke's FastAPI backend structure.
"""

from __future__ import annotations
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.env import BankEmailTriageEnv
from app.models import (
    ResetRequest, ResetResponse,
    StepRequest, StepResult,
    StateResponse, TaskInfo,
    EmailAction, EmailCategory, Priority, Department,
)
from app.tasks import list_tasks, get_task
from app.emails import BANK_EMAILS

# ─────────────────────────────────────────────
# App init
# ─────────────────────────────────────────────

app = FastAPI(
    title="Bank Support Email Triage — OpenEnv",
    description=(
        "OpenEnv-compliant environment for training AI agents on bank customer "
        "support email triage. Implements reset()/step()/state() API. "
        "3 tasks: easy (categorize) → medium (triage+route) → hard (full response). "
        "Domain: Indian retail banking support emails."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single shared environment instance (stateful per session)
env = BankEmailTriageEnv()


# ─────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────

@app.get("/", tags=["health"])
def root():
    return {
        "status": "ok",
        "env": "bank-email-triage-v1",
        "tasks": ["task_1", "task_2", "task_3"],
        "emails": len(BANK_EMAILS),
        "openenv_spec": "1.0",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}


# ─────────────────────────────────────────────
# Task listing
# ─────────────────────────────────────────────

@app.get("/tasks", response_model=list[TaskInfo], tags=["tasks"])
def get_tasks():
    """List all available tasks with descriptions and difficulty."""
    return list_tasks()


@app.get("/tasks/{task_id}", response_model=TaskInfo, tags=["tasks"])
def get_task_info(task_id: str):
    """Get info for a specific task."""
    try:
        return get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─────────────────────────────────────────────
# OpenEnv core API
# ─────────────────────────────────────────────

@app.post("/reset", response_model=ResetResponse, tags=["openenv"])
def reset(request: ResetRequest = ResetRequest()):
    """
    Reset the environment for a new episode.
    Returns the initial observation.
    """
    try:
        result = env.reset(
            task_id=request.task_id,
            email_id=request.email_id,
        )
        return ResetResponse(
            observation=result.observation,
            done=result.done,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step", response_model=StepResult, tags=["openenv"])
def step(request: StepRequest):
    """
    Submit an action and receive reward + next observation.
    Must call /reset before first /step.
    """
    try:
        result = env.step(request.action)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Environment error: {e}")


@app.get("/state", response_model=StateResponse, tags=["openenv"])
def state():
    """Return current internal state of the environment."""
    return StateResponse(state=env.state())


# ─────────────────────────────────────────────
# Convenience endpoints
# ─────────────────────────────────────────────

class EmailSummary(BaseModel):
    email_id: str
    sender: str
    subject: str
    category: str
    priority: str

@app.get("/emails", response_model=list[EmailSummary], tags=["data"])
def list_emails():
    """List all available emails (subject + ground truth for debugging)."""
    return [
        EmailSummary(
            email_id=e.email_id,
            sender=e.sender,
            subject=e.subject,
            category=e.true_category.value,
            priority=e.true_priority.value,
        )
        for e in BANK_EMAILS
    ]


# ─────────────────────────────────────────────
# Entrypoint
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)