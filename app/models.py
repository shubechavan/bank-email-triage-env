"""
Typed Pydantic models for the Bank Support Email Triage OpenEnv environment.
Implements the full OpenEnv spec: Observation, Action, Reward, StepResult.
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# Domain Enums
# ─────────────────────────────────────────────

class EmailCategory(str, Enum):
    FRAUD_DISPUTE    = "fraud_dispute"
    ACCOUNT_INQUIRY  = "account_inquiry"
    LOAN_COMPLAINT   = "loan_complaint"
    CARD_SERVICES    = "card_services"
    GENERAL_FEEDBACK = "general_feedback"
    UNRELATED        = "unrelated"


class Priority(str, Enum):
    HIGH   = "high"
    MEDIUM = "medium"
    LOW    = "low"


class Department(str, Enum):
    FRAUD_TEAM       = "fraud_team"
    ACCOUNT_SERVICES = "account_services"
    LOANS            = "loans"
    CARD_OPERATIONS  = "card_operations"
    CUSTOMER_CARE    = "customer_care"
    NO_ACTION        = "no_action"


# ─────────────────────────────────────────────
# Email model (internal data object)
# ─────────────────────────────────────────────

class BankEmail(BaseModel):
    email_id:   str
    sender:     str
    subject:    str
    body:       str
    timestamp:  str

    # Ground truth labels (hidden from agent, used by grader)
    true_category:   EmailCategory
    true_priority:   Priority
    true_department: Department
    expected_keywords: List[str] = Field(default_factory=list,
        description="Keywords expected in a valid response draft")


# ─────────────────────────────────────────────
# OpenEnv: Observation
# ─────────────────────────────────────────────

class EmailObservation(BaseModel):
    """What the agent sees at each step."""
    email_id:        str
    sender:          str
    subject:         str
    body:            str
    timestamp:       str
    task_id:         str   = Field(description="task_1 | task_2 | task_3")
    task_description: str  = Field(description="Natural language description of what to do")
    step_number:     int
    echoed_message:  Optional[str] = Field(None,
        description="Last action echoed back for logging compatibility")
    available_categories:   List[str] = list(EmailCategory)
    available_priorities:   List[str] = list(Priority)
    available_departments:  List[str] = list(Department)


# ─────────────────────────────────────────────
# OpenEnv: Action
# ─────────────────────────────────────────────

class EmailAction(BaseModel):
    """
    What the agent submits per step.

    For task_1: only category is required.
    For task_2: category + priority + department.
    For task_3: all fields including response_draft.
    """
    category:        EmailCategory
    priority:        Optional[Priority]    = None
    department:      Optional[Department]  = None
    response_draft:  Optional[str]         = Field(None,
        description="Draft reply email body for task_3 (task_3 only)")
    raw_message:     Optional[str]         = Field(None,
        description="Raw string from the model before structured parsing")


# ─────────────────────────────────────────────
# OpenEnv: Reward
# ─────────────────────────────────────────────

class EmailReward(BaseModel):
    """Breakdown of the reward signal."""
    total:             float = Field(..., ge=0.0, le=1.0)
    category_score:    float = Field(0.0, ge=0.0, le=1.0)
    priority_score:    float = Field(0.0, ge=0.0, le=1.0)
    department_score:  float = Field(0.0, ge=0.0, le=1.0)
    response_score:    float = Field(0.0, ge=0.0, le=1.0)
    penalty:           float = Field(0.0, le=0.0)
    feedback:          str   = ""


# ─────────────────────────────────────────────
# OpenEnv: StepResult (returned by step())
# ─────────────────────────────────────────────

class StepResult(BaseModel):
    observation: EmailObservation
    reward:      float
    done:        bool
    info:        Dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────
# OpenEnv: State (returned by state())
# ─────────────────────────────────────────────

class EnvState(BaseModel):
    task_id:       str
    email_id:      str
    step_number:   int
    done:          bool
    total_reward:  float
    reward_history: List[float] = Field(default_factory=list)


# ─────────────────────────────────────────────
# API Request/Response wrappers
# ─────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: str = Field("task_1",
        description="Which task to load: task_1 | task_2 | task_3")
    email_id: Optional[str] = Field(None,
        description="Optional specific email ID; random if omitted")


class ResetResponse(BaseModel):
    observation: EmailObservation
    done:        bool = False


class StepRequest(BaseModel):
    action: EmailAction


class StateResponse(BaseModel):
    state: EnvState


class TaskInfo(BaseModel):
    task_id:     str
    name:        str
    description: str
    difficulty:  str
    max_steps:   int
    reward_breakdown: Dict[str, float]