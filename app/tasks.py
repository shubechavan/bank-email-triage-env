"""
Three tasks with deterministic graders for the Bank Email Triage OpenEnv.

Task 1 (Easy)   — Email categorization only
Task 2 (Medium) — Categorization + Priority + Department routing
Task 3 (Hard)   — Full triage + RAG-informed response draft quality

Graders return EmailReward with scores 0.0–1.0.
Reward is shaped (partial credit) not binary.
"""

from __future__ import annotations
from typing import List
from app.models import (
    BankEmail, EmailAction, EmailReward,
    EmailCategory, Priority, Department, TaskInfo,
)
from app.bank_kb import get_policy_for_category


# ─────────────────────────────────────────────
# Task metadata
# ─────────────────────────────────────────────

TASK_REGISTRY: dict[str, TaskInfo] = {
    "task_1": TaskInfo(
        task_id="task_1",
        name="Bank Email Categorization",
        description=(
            "Read the bank support email and assign the correct category. "
            "Categories: fraud_dispute, account_inquiry, loan_complaint, "
            "card_services, general_feedback, unrelated."
        ),
        difficulty="easy",
        max_steps=1,
        reward_breakdown={"category": 1.0},
    ),
    "task_2": TaskInfo(
        task_id="task_2",
        name="Bank Email Triage & Routing",
        description=(
            "Read the bank support email and provide: "
            "(1) correct category, (2) priority level (high/medium/low), "
            "(3) correct department to route to. "
            "All three fields are required."
        ),
        difficulty="medium",
        max_steps=1,
        reward_breakdown={"category": 0.4, "priority": 0.3, "department": 0.3},
    ),
    "task_3": TaskInfo(
        task_id="task_3",
        name="Bank Email Full Response",
        description=(
            "Read the bank support email and provide: "
            "(1) correct category, (2) priority level, (3) correct department, "
            "(4) a professional response_draft email to send to the customer. "
            "The response must acknowledge the issue, reference bank policy, "
            "and provide actionable next steps."
        ),
        difficulty="hard",
        max_steps=1,
        reward_breakdown={
            "category": 0.2,
            "priority": 0.2,
            "department": 0.2,
            "response_quality": 0.4,
        },
    ),
}


# ─────────────────────────────────────────────
# Helper grading functions
# ─────────────────────────────────────────────

def _score_category(action: EmailAction, email: BankEmail) -> float:
    """Exact match on category. No partial credit — wrong category = 0.01."""
    return 0.99 if action.category == email.true_category else 0.01


def _score_priority(action: EmailAction, email: BankEmail) -> float:
    """
    Priority scoring with partial credit:
    - Exact match: 0.99
    - One level off (e.g. HIGH predicted as MEDIUM): 0.4
    - Two levels off (HIGH predicted as LOW): 0.01
    """
    if action.priority is None:
        return 0.01
    levels = [Priority.HIGH, Priority.MEDIUM, Priority.LOW]
    try:
        pred_idx = levels.index(action.priority)
        true_idx = levels.index(email.true_priority)
        diff = abs(pred_idx - true_idx)
        if diff == 0:
            return 0.99
        elif diff == 1:
            return 0.4
        else:
            return 0.01
    except ValueError:
        return 0.01


def _score_department(action: EmailAction, email: BankEmail) -> float:
    """Exact match on department. No partial credit — routing matters."""
    if action.department is None:
        return 0.01
    return 0.99 if action.department == email.true_department else 0.01


def _score_response(action: EmailAction, email: BankEmail) -> float:
    """
    Response draft quality scoring (task_3 only):

    Checks:
    1. Non-empty and minimum length (>50 words)            → 0.10
    2. Professional greeting/closing                        → 0.10
    3. Acknowledges the specific issue from email body     → 0.20
    4. Contains expected keywords from bank KB             → 0.30
    5. Mentions next steps / resolution timeline           → 0.20
    6. Penalty if response is generic/templated            → -0.10

    Max: 0.90 (clamped to 1.0)
    Penalty applied after: can go to 0.80 minimum if all criteria met.
    """
    if not action.response_draft:
        return 0.0

    draft = action.response_draft.lower()
    words = draft.split()
    score = 0.0

    # 1. Minimum length (>50 words signals meaningful response)
    if len(words) >= 50:
        score += 0.10
    elif len(words) >= 20:
        score += 0.05

    # 2. Professional greeting + closing
    has_greeting = any(g in draft for g in ["dear", "hello", "hi ", "greetings"])
    has_closing  = any(c in draft for c in ["regards", "sincerely", "thank you", "best", "yours"])
    if has_greeting:
        score += 0.05
    if has_closing:
        score += 0.05

    # 3. Acknowledges specific issue (uses subject/key nouns from email body)
    body_keywords = _extract_key_nouns(email.body)
    subject_keywords = _extract_key_nouns(email.subject)
    combined = body_keywords | subject_keywords
    matched_body = sum(1 for kw in combined if kw in draft)
    if matched_body >= 3:
        score += 0.20
    elif matched_body >= 1:
        score += 0.10

    # 4. Contains expected_keywords from email ground truth
    matched_expected = sum(
        1 for kw in email.expected_keywords
        if kw.lower() in draft
    )
    kw_ratio = matched_expected / max(len(email.expected_keywords), 1)
    score += 0.30 * kw_ratio

    # 5. Next steps / timeline / action
    action_words = [
        "within", "working day", "days", "process", "resolve", "escalat",
        "contact", "call", "visit", "submit", "upload", "check", "track",
        "24 hours", "48 hours", "we will", "our team", "please",
    ]
    action_count = sum(1 for aw in action_words if aw in draft)
    if action_count >= 4:
        score += 0.20
    elif action_count >= 2:
        score += 0.10

    # 6. Penalty for overly generic responses (no email-specific content)
    generic_phrases = [
        "we apologize for the inconvenience",
        "please contact our customer service",
        "thank you for contacting us",
    ]
    generic_count = sum(1 for gp in generic_phrases if gp in draft)
    if generic_count >= 2 and matched_body == 0:
        score -= 0.10  # Penalize pure-template responses with no specificity

    return round(min(max(score, 0.01), 0.99), 3)


def _extract_key_nouns(text: str) -> set:
    """
    Simple noun extraction — grabs capitalized words and banking terms.
    Used to check if response acknowledges the email's specific content.
    """
    banking_terms = {
        "account", "card", "loan", "emi", "transfer", "neft", "atm",
        "fraud", "unauthorized", "transaction", "balance", "credit",
        "debit", "statement", "kyc", "otp", "password", "interest",
        "disbursement", "foreclosure", "reward", "block", "limit",
        "international", "swift", "payment", "due", "branch",
    }
    words = text.lower().split()
    return {w.strip(".,!?;:()") for w in words if w.strip(".,!?;:()") in banking_terms}


# ─────────────────────────────────────────────
# Main Grader functions — one per task
# ─────────────────────────────────────────────

def grade_task_1(action: EmailAction, email: BankEmail) -> EmailReward:
    """
    Task 1 Grader — Categorization only.
    Score: 1.0 for correct category, 0.0 for wrong.
    """
    cat_score = _score_category(action, email)
    penalty = 0.0

    # Small penalty for providing unrequested fields incorrectly
    # (agent should focus only on category)
    if action.response_draft and len(action.response_draft) > 10:
        penalty = -0.0  # No penalty, just ignore extra fields in task_1

    total = round(min(max(cat_score + penalty, 0.01), 0.99), 3)
    feedback = (
        f"Category: {'✓ correct' if cat_score >= 0.99 else f'✗ wrong (got {action.category}, expected {email.true_category})'}"
    )
    return EmailReward(
        total=total,
        category_score=cat_score,
        priority_score=0.01,
        department_score=0.01,
        response_score=0.01,
        penalty=penalty,
        feedback=feedback,
    )


def grade_task_2(action: EmailAction, email: BankEmail) -> EmailReward:
    """
    Task 2 Grader — Triage + Routing.
    Weighted: category(0.4) + priority(0.3) + department(0.3)
    """
    cat_score  = _score_category(action, email)
    pri_score  = _score_priority(action, email)
    dept_score = _score_department(action, email)

    # Penalty: if category wrong AND department wrong = double-wrong is penalized
    penalty = 0.0
    if cat_score == 0.0 and dept_score == 0.0:
        penalty = -0.05  # Minor penalty for completely wrong routing

    total = round(
        min(max(
            0.4 * cat_score + 0.3 * pri_score + 0.3 * dept_score + penalty,
            0.01
        ), 0.99),
        3,
    )

    feedback_parts = [
        f"Category: {'✓' if cat_score >= 0.99 else f'✗ (got {action.category}, expected {email.true_category})'}",
        f"Priority: {'✓' if pri_score >= 0.99 else f'partial({pri_score})' if pri_score > 0 else f'✗ (got {action.priority}, expected {email.true_priority})'}",
        f"Department: {'✓' if dept_score >= 0.99 else f'✗ (got {action.department}, expected {email.true_department})'}",
    ]
    return EmailReward(
        total=total,
        category_score=cat_score,
        priority_score=pri_score,
        department_score=dept_score,
        response_score=0.01,
        penalty=penalty,
        feedback=" | ".join(feedback_parts),
    )


def grade_task_3(action: EmailAction, email: BankEmail) -> EmailReward:
    """
    Task 3 Grader — Full triage + response draft.
    Weighted: category(0.2) + priority(0.2) + department(0.2) + response(0.4)
    """
    cat_score  = _score_category(action, email)
    pri_score  = _score_priority(action, email)
    dept_score = _score_department(action, email)
    resp_score = _score_response(action, email)

    # Penalty: Empty or very short response
    penalty = 0.0
    if not action.response_draft or len(action.response_draft.split()) < 20:
        penalty = -0.10  # Penalize missing/trivial response for hard task

    total = round(
        min(max(
            0.2 * cat_score +
            0.2 * pri_score +
            0.2 * dept_score +
            0.4 * resp_score +
            penalty,
            0.01
        ), 0.99),
        3,
    )

    feedback_parts = [
        f"Category: {'✓' if cat_score >= 0.99 else f'✗({action.category})'}",
        f"Priority: {'✓' if pri_score >= 0.99 else f'~({pri_score})' if pri_score > 0.01 else f'✗({action.priority})'}",
        f"Dept: {'✓' if dept_score >= 0.99 else f'✗({action.department})'}",
        f"Response quality: {resp_score:.2f}/0.99",
    ]
    return EmailReward(
        total=total,
        category_score=cat_score,
        priority_score=pri_score,
        department_score=dept_score,
        response_score=resp_score,
        penalty=penalty,
        feedback=" | ".join(feedback_parts),
    )


# ─────────────────────────────────────────────
# Dispatcher
# ─────────────────────────────────────────────

GRADERS = {
    "task_1": grade_task_1,
    "task_2": grade_task_2,
    "task_3": grade_task_3,
}


def grade(task_id: str, action: EmailAction, email: BankEmail) -> EmailReward:
    """Route to correct grader by task_id."""
    grader = GRADERS.get(task_id)
    if not grader:
        raise ValueError(f"Unknown task_id: {task_id}")
    return grader(action, email)


def list_tasks() -> List[TaskInfo]:
    return list(TASK_REGISTRY.values())


def get_task(task_id: str) -> TaskInfo:
    task = TASK_REGISTRY.get(task_id)
    if not task:
        raise ValueError(f"Unknown task_id: {task_id}. Valid: {list(TASK_REGISTRY.keys())}")
    return task