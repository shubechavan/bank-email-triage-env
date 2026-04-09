"""
Core OpenEnv environment for Bank Support Email Triage.
Implements: reset() / step() / state() per OpenEnv spec.

Design inspired by:
- mailflow: multi-agent email pipeline (categorize → QA → respond)
- sanikasalunke RAG agent: FastAPI + multi-turn state management
"""

from __future__ import annotations
import random
from typing import Optional

from app.models import (
    BankEmail, EmailAction, EmailObservation,
    EnvState, StepResult, EmailCategory, Priority, Department,
)
from app.emails import BANK_EMAILS, EMAIL_INDEX
from app.tasks import grade, get_task, TASK_REGISTRY


class BankEmailTriageEnv:
    """
    OpenEnv-compliant environment for Bank Support Email Triage.

    Episode structure:
    - Each episode = one email + one task
    - Agent gets one step to submit its action (max_steps=1 per task)
    - reset() loads a fresh email + task
    - step() scores the action and marks done=True
    - state() returns current internal state at any point

    Reward is always in [0.0, 1.0] — shaped by the task grader.
    """

    def __init__(self):
        self._current_email: Optional[BankEmail] = None
        self._task_id: str = "task_1"
        self._step_number: int = 0
        self._done: bool = False
        self._total_reward: float = 0.0
        self._reward_history: list[float] = []
        self._last_observation: Optional[EmailObservation] = None

    # ─────────────────────────────────────────────
    # reset()
    # ─────────────────────────────────────────────

    def reset(
        self,
        task_id: str = "task_1",
        email_id: Optional[str] = None,
    ) -> StepResult:
        """
        Reset the environment for a new episode.

        Args:
            task_id:  Which task to run (task_1 | task_2 | task_3)
            email_id: Specific email to load (random if None)

        Returns:
            StepResult with initial observation, reward=0.0, done=False
        """
        # Validate task
        get_task(task_id)  # raises ValueError if invalid

        # Pick email
        if email_id:
            email = EMAIL_INDEX.get(email_id)
            if not email:
                raise ValueError(f"Email ID '{email_id}' not found.")
        else:
            email = random.choice(BANK_EMAILS)

        self._current_email = email
        self._task_id = task_id
        self._step_number = 0
        self._done = False
        self._total_reward = 0.0
        self._reward_history = []

        obs = self._build_observation(echo=None)
        self._last_observation = obs

        return StepResult(
            observation=obs,
            reward=0.01,
            done=False,
            info={"message": "Environment reset. Submit your action via step()."},
        )

    # ─────────────────────────────────────────────
    # step()
    # ─────────────────────────────────────────────

    def step(self, action: EmailAction) -> StepResult:
        """
        Submit an action and receive reward + next observation.

        Args:
            action: EmailAction with category (+ optional priority/dept/response)

        Returns:
            StepResult with observation, reward, done=True (single-step tasks)
        """
        if self._done:
            # Episode already finished — return terminal observation
            obs = self._build_observation(echo=str(action.category))
            return StepResult(
                observation=obs,
                reward=0.01,
                done=True,
                info={"warning": "Episode already done. Call reset() to start a new episode."},
            )

        if self._current_email is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")

        self._step_number += 1

        # Grade the action
        reward_obj = grade(self._task_id, action, self._current_email)
        reward = reward_obj.total

        self._total_reward += reward
        self._reward_history.append(reward)
        self._done = True  # Single-step episode: done after first action

        # Build echo for logging compatibility (matches sample inference.py pattern)
        echo = self._build_echo(action)
        obs = self._build_observation(echo=echo)
        self._last_observation = obs

        return StepResult(
            observation=obs,
            reward=reward,
            done=True,
            info={
                "reward_breakdown": reward_obj.model_dump(),
                "true_category":    self._current_email.true_category.value,
                "true_priority":    self._current_email.true_priority.value,
                "true_department":  self._current_email.true_department.value,
                "feedback":         reward_obj.feedback,
            },
        )

    # ─────────────────────────────────────────────
    # state()
    # ─────────────────────────────────────────────

    def state(self) -> EnvState:
        """Return current internal state of the environment."""
        return EnvState(
            task_id=self._task_id,
            email_id=self._current_email.email_id if self._current_email else "none",
            step_number=self._step_number,
            done=self._done,
            total_reward=self._total_reward,
            reward_history=self._reward_history,
        )

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────

    def _build_observation(self, echo: Optional[str]) -> EmailObservation:
        """Construct an EmailObservation from current state."""
        task_info = TASK_REGISTRY[self._task_id]
        email = self._current_email

        return EmailObservation(
            email_id=email.email_id,
            sender=email.sender,
            subject=email.subject,
            body=email.body,
            timestamp=email.timestamp,
            task_id=self._task_id,
            task_description=task_info.description,
            step_number=self._step_number,
            echoed_message=echo,
            available_categories=[c.value for c in EmailCategory],
            available_priorities=[p.value for p in Priority],
            available_departments=[d.value for d in Department],
        )

    def _build_echo(self, action: EmailAction) -> str:
        """Build a human-readable echo of the agent's action for logging."""
        parts = [f"category={action.category.value}"]
        if action.priority:
            parts.append(f"priority={action.priority.value}")
        if action.department:
            parts.append(f"department={action.department.value}")
        if action.response_draft:
            preview = action.response_draft[:80].replace("\n", " ")
            parts.append(f"draft_preview='{preview}...'")
        return " | ".join(parts)