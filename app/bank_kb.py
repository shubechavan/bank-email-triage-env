"""
Bank Knowledge Base — lightweight in-memory RAG substitute.
Inspired by mailflow's RAG agency.txt + sanikasalunke's FAISS KB.
No heavy dependencies (no FAISS, no embeddings) — simple keyword lookup.
Used by the task_3 grader to evaluate response quality.
"""

from typing import List

# ─────────────────────────────────────────────────────────────────────────────
# Bank Policy & FAQ Knowledge Base
# Each entry: (category_tags, policy_text)
# ─────────────────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE: List[dict] = [

    # FRAUD & DISPUTE
    {
        "tags": ["fraud", "unauthorized", "dispute", "chargeback", "block"],
        "content": (
            "For unauthorized transactions: Block the account/card immediately. "
            "Raise a chargeback within 7 working days. Disputes are investigated "
            "within 10–14 working days per RBI guidelines. Provide a provisional "
            "credit within 5 days for transactions above ₹5,000. "
            "Customer must file a complaint via email or branch within 3 days of noticing fraud."
        ),
    },
    {
        "tags": ["phishing", "credentials", "compromised", "password", "net banking"],
        "content": (
            "If credentials are compromised: Reset net banking password immediately. "
            "Disable all active sessions. Check for suspicious transactions in the last 48 hours. "
            "Customer should contact cyber fraud helpline 1930. "
            "Issue new net banking credentials within 24 hours."
        ),
    },
    {
        "tags": ["ATM", "dispense", "cash", "shortfall", "receipt"],
        "content": (
            "ATM cash shortfall: Raised disputes are resolved within 5 working days per RBI. "
            "Refund is auto-credited if ATM records confirm shortfall. "
            "Customer should retain receipt. Claim must be filed within 30 days of transaction."
        ),
    },
    {
        "tags": ["NEFT", "transfer", "failed", "not received", "beneficiary"],
        "content": (
            "Failed NEFT transactions: If not credited within 2 hours, amount is "
            "auto-reversed within 24 hours per RBI mandate. "
            "Customer can raise a trace request with UTR number. "
            "Refund timeline: T+1 working day for domestic transfers."
        ),
    },

    # ACCOUNT SERVICES
    {
        "tags": ["statement", "account", "6 months", "PDF", "email"],
        "content": (
            "Account statements can be downloaded via net banking or mobile app for up to 2 years. "
            "For physical statements, visit branch or request via email. "
            "E-statements are sent to registered email free of charge. "
            "For home loan/tax purposes, Form 16A can be requested separately."
        ),
    },
    {
        "tags": ["mobile", "update", "KYC", "number", "OTP"],
        "content": (
            "Mobile number update: Can be done via branch with Aadhaar + OTP verification. "
            "Online update available via net banking if current mobile is accessible. "
            "KYC update required every 2 years. Documents: Aadhaar, PAN, address proof. "
            "Process takes 2 working days."
        ),
    },
    {
        "tags": ["international", "wire", "SWIFT", "transfer", "charges", "forex"],
        "content": (
            "International wire transfers: Charges are ₹500–₹2,000 + correspondent bank fees. "
            "SWIFT transfers take 2–5 working days. "
            "Daily limit: ₹5,00,000 equivalent without prior approval. "
            "Documents required: PAN, purpose declaration, beneficiary bank details. "
            "Exchange rate is applied at time of processing."
        ),
    },
    {
        "tags": ["KYC", "documents", "pending", "restriction", "Aadhaar", "PAN"],
        "content": (
            "KYC documents required: Aadhaar card (mandatory), PAN card, recent photograph, "
            "address proof (utility bill/passport). "
            "KYC can be completed via: (1) Branch visit, (2) Video KYC on mobile app, "
            "(3) Aadhaar-based e-KYC online. "
            "Account restrictions are lifted within 24 hours of successful KYC."
        ),
    },
    {
        "tags": ["joint account", "spouse", "savings", "open", "minimum balance"],
        "content": (
            "Joint savings account: Minimum balance ₹5,000 (metro branches), ₹2,000 (rural). "
            "Documents: Aadhaar + PAN for both account holders, photographs. "
            "Mode of operation: Either or Survivor / Joint. "
            "Can be opened at any branch or started online (in-person verification required)."
        ),
    },

    # LOANS
    {
        "tags": ["EMI", "double", "debit", "refund", "overdraft", "loan"],
        "content": (
            "Duplicate EMI debit: Reversal processed within 2 working days. "
            "Overdraft charges caused by bank error are waived. "
            "Customer receives written confirmation and SMS notification of reversal. "
            "Escalation to loan operations team for same-day resolution on high-priority cases."
        ),
    },
    {
        "tags": ["foreclosure", "charges", "prepayment", "principal", "RBI"],
        "content": (
            "Loan foreclosure charges: As per RBI guidelines, no foreclosure charges on "
            "floating rate loans for individuals. Fixed rate loans: 2% of outstanding principal. "
            "Partial prepayment allowed after 6 EMIs without charges. "
            "Foreclosure statement generated within 3 working days."
        ),
    },
    {
        "tags": ["application", "loan", "status", "pending", "car loan", "process"],
        "content": (
            "Loan application process: Standard processing time is 7–10 working days after "
            "document submission. Car loan approval: 3–5 days. Home loan: 15–20 days. "
            "Status can be checked via net banking or by calling 1800-XXX-XXXX. "
            "Missing documents are the most common cause of delays."
        ),
    },
    {
        "tags": ["interest rate", "home loan", "EMI increase", "revision", "floating"],
        "content": (
            "Loan interest rate changes: Floating rate loans are linked to the bank's MCLR/EBLR. "
            "Rate revisions are communicated 30 days in advance via registered email and SMS. "
            "If no communication was received, customer can request waiver of increased EMI "
            "for one month while investigation is conducted."
        ),
    },
    {
        "tags": ["education loan", "disbursement", "sanction", "college", "semester"],
        "content": (
            "Education loan disbursement: After sanction, disbursement is made directly to "
            "institution within 5 working days on receipt of fee demand letter. "
            "Student must submit: Admission letter, fee receipt, institution bank details. "
            "Expedited processing available for urgent cases — escalate to loans manager."
        ),
    },

    # CARD SERVICES
    {
        "tags": ["block", "lost", "card", "replacement", "hotlist", "debit"],
        "content": (
            "Lost/stolen card: Card can be blocked via: mobile app, net banking, "
            "IVR 1800-XXX-XXXX, or email support. Block is immediate. "
            "Replacement card issued within 5–7 working days. "
            "Replacement charges: ₹200 (debit card), ₹500 (credit card). "
            "Emergency card available at select branches."
        ),
    },
    {
        "tags": ["credit card", "statement", "bill", "due date", "payment"],
        "content": (
            "Credit card statement: Available on mobile app and net banking. "
            "Physical statement sent to registered address by 5th of each month. "
            "E-statement sent to registered email. Minimum due is 5% of outstanding balance. "
            "Late payment fee: ₹500–₹1,200 depending on balance. Grace period: 3 days."
        ),
    },
    {
        "tags": ["credit limit", "increase", "request", "eligibility"],
        "content": (
            "Credit limit increase: Eligible after 6 months of card usage with clean payment history. "
            "Apply via mobile app or net banking. Approval based on credit score (min 750) and income. "
            "Temporary limit increase available for specific purchases. "
            "Permanent increase processed in 5–7 working days."
        ),
    },
    {
        "tags": ["international", "card", "abroad", "activate", "foreign", "enable"],
        "content": (
            "International card usage: Enable via mobile app → Card Settings → International Transactions. "
            "Or call 1800-XXX-XXXX. Activation is immediate. "
            "Set daily international limit before travel. "
            "Inform bank of travel dates to avoid fraud blocks. "
            "Forex markup: 3.5% on transactions outside India."
        ),
    },
    {
        "tags": ["reward points", "credit", "purchase", "missing", "loyalty"],
        "content": (
            "Reward points: Credited within 3 working days of transaction. "
            "Not applicable on fuel, insurance, and government transactions. "
            "Missing points dispute must be raised within 60 days. "
            "Points can be redeemed on app for cashback, vouchers, or air miles."
        ),
    },

    # GENERAL FEEDBACK
    {
        "tags": ["app", "mobile", "slow", "crash", "bug", "technical"],
        "content": (
            "App issues: Reported to technical team for resolution within 48–72 hours. "
            "Customers advised to update to latest app version and clear cache. "
            "Critical bugs are prioritized and hotfixed within 24 hours. "
            "Status updates shared via social media and in-app notifications."
        ),
    },
    {
        "tags": ["staff", "rude", "branch", "complaint", "behavior"],
        "content": (
            "Staff complaints: Acknowledged within 24 hours. Forwarded to branch manager. "
            "Investigation conducted and response provided within 7 working days. "
            "Customer is compensated with apology and any incurred charges waived. "
            "Action taken against staff as per HR policy."
        ),
    },
    {
        "tags": ["suggestion", "feature", "UPI", "feedback", "improvement"],
        "content": (
            "Customer suggestions are logged and shared with product team. "
            "Customers receive acknowledgement email within 24 hours. "
            "Feature requests reviewed in quarterly product planning cycle. "
            "Valuable suggestions may be rewarded with loyalty points."
        ),
    },
    {
        "tags": ["ATM", "out of cash", "replenish", "weekend", "operations"],
        "content": (
            "ATM cash replenishment: Escalated to ATM operations team immediately. "
            "Standard replenishment cycle is daily. Weekends see higher demand — "
            "additional cash loading scheduled for Friday evenings at high-usage ATMs. "
            "Customer can report ATM issues via app or 1800-XXX-XXXX."
        ),
    },
]


def search_kb(query_tags: List[str], top_k: int = 2) -> List[str]:
    """
    Simple keyword overlap search across the knowledge base.
    Returns top_k most relevant policy texts.
    Used by task_3 grader to check if response aligns with bank policies.
    """
    scored = []
    query_lower = {t.lower() for t in query_tags}
    for entry in KNOWLEDGE_BASE:
        tags_lower = {t.lower() for t in entry["tags"]}
        overlap = len(query_lower & tags_lower)
        if overlap > 0:
            scored.append((overlap, entry["content"]))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [content for _, content in scored[:top_k]]


def get_policy_for_category(category: str) -> List[str]:
    """Return all KB entries relevant to a given email category."""
    category_tag_map = {
        "fraud_dispute":    ["fraud", "unauthorized", "phishing", "ATM", "NEFT"],
        "account_inquiry":  ["statement", "mobile", "international", "KYC", "joint account"],
        "loan_complaint":   ["EMI", "foreclosure", "application", "interest rate", "education loan"],
        "card_services":    ["block", "credit card", "credit limit", "international", "reward points"],
        "general_feedback": ["app", "staff", "suggestion", "ATM"],
        "unrelated":        [],
    }
    tags = category_tag_map.get(category, [])
    return search_kb(tags, top_k=3)