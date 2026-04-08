"""
Synthetic bank customer support email dataset.
30 emails across 6 categories with ground-truth labels.
Inspired by real banking support workflows (mailflow categorization + bank domain).
"""

from app.models import BankEmail, EmailCategory, Priority, Department

BANK_EMAILS: list[BankEmail] = [

    # ── FRAUD_DISPUTE (HIGH priority → fraud_team) ────────────────────────
    BankEmail(
        email_id="E001",
        sender="rahul.sharma@gmail.com",
        subject="Unauthorized transaction on my savings account",
        body=(
            "Dear Support,\n\n"
            "I noticed a transaction of ₹45,000 on my savings account (ending 4521) "
            "dated 07-Apr-2026 that I did not authorize. I was in Mumbai at that time "
            "and have not shared my OTP or PIN with anyone. Please block my account "
            "immediately and initiate a chargeback. This is very urgent.\n\n"
            "Account holder: Rahul Sharma\nAccount: XXXX4521"
        ),
        timestamp="2026-04-08T08:15:00Z",
        true_category=EmailCategory.FRAUD_DISPUTE,
        true_priority=Priority.HIGH,
        true_department=Department.FRAUD_TEAM,
        expected_keywords=["block", "chargeback", "investigate", "unauthorized", "secure"],
    ),
    BankEmail(
        email_id="E002",
        sender="priya.mehta@yahoo.com",
        subject="Someone used my card without my knowledge",
        body=(
            "Hello,\n\n"
            "Three transactions totaling ₹12,500 appeared on my credit card statement "
            "that I did not make. These are from an online merchant I've never used. "
            "Please dispute these charges and issue a new card. My card number ends in 8834.\n\n"
            "Regards,\nPriya Mehta"
        ),
        timestamp="2026-04-08T09:00:00Z",
        true_category=EmailCategory.FRAUD_DISPUTE,
        true_priority=Priority.HIGH,
        true_department=Department.FRAUD_TEAM,
        expected_keywords=["dispute", "new card", "block", "fraud", "investigate"],
    ),
    BankEmail(
        email_id="E003",
        sender="ajay.verma@hotmail.com",
        subject="Phishing attempt — my credentials may be compromised",
        body=(
            "Hi,\n\n"
            "I accidentally clicked a link in an email that looked like it was from "
            "your bank. I may have entered my net banking credentials. Please reset "
            "my password, disable my current login session, and check for any "
            "suspicious activity on my account (Acc: XXXX7712).\n\nThanks,\nAjay"
        ),
        timestamp="2026-04-07T22:45:00Z",
        true_category=EmailCategory.FRAUD_DISPUTE,
        true_priority=Priority.HIGH,
        true_department=Department.FRAUD_TEAM,
        expected_keywords=["reset", "password", "suspicious", "secure", "block session"],
    ),
    BankEmail(
        email_id="E004",
        sender="sunita.rao@gmail.com",
        subject="Money debited but not received by beneficiary",
        body=(
            "Dear Team,\n\n"
            "I transferred ₹8,000 to my friend's account via NEFT yesterday "
            "(Ref: NEFT20260407091234) but the amount was debited from my account "
            "and the beneficiary has not received it. Please investigate and refund "
            "if not credited within 24 hours.\n\nSunita Rao"
        ),
        timestamp="2026-04-08T10:30:00Z",
        true_category=EmailCategory.FRAUD_DISPUTE,
        true_priority=Priority.HIGH,
        true_department=Department.FRAUD_TEAM,
        expected_keywords=["investigate", "refund", "NEFT", "trace", "credit"],
    ),
    BankEmail(
        email_id="E005",
        sender="mohan.krishna@gmail.com",
        subject="ATM dispensed less cash than debited",
        body=(
            "Hello Support,\n\n"
            "I withdrew ₹10,000 from your ATM (ID: ATM-MUM-0042) at 7pm yesterday "
            "but only ₹9,500 was dispensed. My account was debited the full ₹10,000. "
            "Please refund the ₹500 difference. I have the ATM receipt as proof.\n\n"
            "Mohan Krishna"
        ),
        timestamp="2026-04-08T11:00:00Z",
        true_category=EmailCategory.FRAUD_DISPUTE,
        true_priority=Priority.HIGH,
        true_department=Department.FRAUD_TEAM,
        expected_keywords=["refund", "ATM", "dispense", "difference", "receipt"],
    ),

    # ── ACCOUNT_INQUIRY (MEDIUM priority → account_services) ──────────────
    BankEmail(
        email_id="E006",
        sender="neha.gupta@gmail.com",
        subject="Request for account statement — last 6 months",
        body=(
            "Hi,\n\nCould you please send me my account statement for the last 6 months "
            "(Oct 2025 – Mar 2026)? I need it for my income tax filing. "
            "Account number ending in 3301.\n\nThank you,\nNeha Gupta"
        ),
        timestamp="2026-04-08T07:00:00Z",
        true_category=EmailCategory.ACCOUNT_INQUIRY,
        true_priority=Priority.MEDIUM,
        true_department=Department.ACCOUNT_SERVICES,
        expected_keywords=["statement", "email", "6 months", "generate", "PDF"],
    ),
    BankEmail(
        email_id="E007",
        sender="vikram.joshi@outlook.com",
        subject="How do I update my registered mobile number?",
        body=(
            "Dear Bank,\n\nI recently changed my mobile number and need to update it "
            "in your records so I can receive OTPs. What is the process? "
            "Do I need to visit a branch or can it be done online?\n\nVikram Joshi"
        ),
        timestamp="2026-04-08T08:45:00Z",
        true_category=EmailCategory.ACCOUNT_INQUIRY,
        true_priority=Priority.MEDIUM,
        true_department=Department.ACCOUNT_SERVICES,
        expected_keywords=["update", "mobile", "KYC", "branch", "online", "OTP"],
    ),
    BankEmail(
        email_id="E008",
        sender="ananya.singh@gmail.com",
        subject="What are the charges for international wire transfer?",
        body=(
            "Hello,\n\nI need to send money to the USA. What are the charges and "
            "exchange rates for international wire transfers? Is there a daily limit? "
            "What documents are required?\n\nAnanya Singh"
        ),
        timestamp="2026-04-08T09:30:00Z",
        true_category=EmailCategory.ACCOUNT_INQUIRY,
        true_priority=Priority.MEDIUM,
        true_department=Department.ACCOUNT_SERVICES,
        expected_keywords=["charges", "wire transfer", "exchange rate", "limit", "SWIFT"],
    ),
    BankEmail(
        email_id="E009",
        sender="deepak.nair@gmail.com",
        subject="KYC update pending — what documents do I need?",
        body=(
            "Hi Support,\n\nI got an SMS saying my KYC is pending and my account "
            "may be restricted. What documents do I need to submit and where? "
            "Can I do it online via your app?\n\nDeepak Nair"
        ),
        timestamp="2026-04-07T16:00:00Z",
        true_category=EmailCategory.ACCOUNT_INQUIRY,
        true_priority=Priority.MEDIUM,
        true_department=Department.ACCOUNT_SERVICES,
        expected_keywords=["KYC", "documents", "Aadhaar", "PAN", "upload", "app"],
    ),
    BankEmail(
        email_id="E010",
        sender="kavita.patel@rediffmail.com",
        subject="Want to open a joint account with my spouse",
        body=(
            "Dear Team,\n\nMy husband and I would like to open a joint savings account. "
            "What are the eligibility criteria and documents needed? "
            "Is there a minimum balance requirement?\n\nKavita Patel"
        ),
        timestamp="2026-04-08T10:00:00Z",
        true_category=EmailCategory.ACCOUNT_INQUIRY,
        true_priority=Priority.LOW,
        true_department=Department.ACCOUNT_SERVICES,
        expected_keywords=["joint account", "documents", "minimum balance", "eligibility", "savings"],
    ),

    # ── LOAN_COMPLAINT (HIGH/MEDIUM → loans) ──────────────────────────────
    BankEmail(
        email_id="E011",
        sender="ramesh.iyer@gmail.com",
        subject="Double EMI deducted from my account this month",
        body=(
            "Hello,\n\nMy home loan EMI of ₹22,000 was debited TWICE from my account "
            "on 5th April 2026. Loan account: HL-2023-00892. This has caused my account "
            "to go into overdraft. Please reverse the extra debit immediately and "
            "ensure this doesn't happen again.\n\nRamesh Iyer"
        ),
        timestamp="2026-04-08T07:30:00Z",
        true_category=EmailCategory.LOAN_COMPLAINT,
        true_priority=Priority.HIGH,
        true_department=Department.LOANS,
        expected_keywords=["reverse", "refund", "EMI", "overdraft", "credit", "apologize"],
    ),
    BankEmail(
        email_id="E012",
        sender="shalini.desai@gmail.com",
        subject="Loan foreclosure charges are too high",
        body=(
            "Dear Sir/Madam,\n\nI want to foreclose my personal loan (PL-2024-00341) "
            "but the charges quoted are 4% of outstanding principal which seems excessive. "
            "RBI guidelines say foreclosure charges should be minimal for floating rate loans. "
            "Please clarify and waive the charges.\n\nShalini Desai"
        ),
        timestamp="2026-04-07T14:00:00Z",
        true_category=EmailCategory.LOAN_COMPLAINT,
        true_priority=Priority.MEDIUM,
        true_department=Department.LOANS,
        expected_keywords=["foreclosure", "charges", "RBI", "waive", "outstanding"],
    ),
    BankEmail(
        email_id="E013",
        sender="ajit.kumar@gmail.com",
        subject="My loan application has been pending for 3 weeks",
        body=(
            "Hello,\n\nI applied for a car loan on 18th March 2026 (Application ID: CAR-2026-5521) "
            "and have not heard back. I submitted all documents including salary slips, "
            "IT returns, and RC. What is the status? This delay is very inconvenient.\n\nAjit Kumar"
        ),
        timestamp="2026-04-08T09:00:00Z",
        true_category=EmailCategory.LOAN_COMPLAINT,
        true_priority=Priority.MEDIUM,
        true_department=Department.LOANS,
        expected_keywords=["status", "application", "pending", "process", "update"],
    ),
    BankEmail(
        email_id="E014",
        sender="pooja.sharma@gmail.com",
        subject="Interest rate on my loan increased without notice",
        body=(
            "Dear Bank,\n\nI noticed my home loan interest rate changed from 8.5% to 9.2% "
            "without any prior communication. This change increased my EMI by ₹3,200 per month. "
            "I was not informed about this revision. Please explain and revert if it was an error.\n\n"
            "Pooja Sharma, Loan Acc: HL-2022-04421"
        ),
        timestamp="2026-04-07T11:00:00Z",
        true_category=EmailCategory.LOAN_COMPLAINT,
        true_priority=Priority.MEDIUM,
        true_department=Department.LOANS,
        expected_keywords=["interest rate", "EMI", "notify", "revert", "explain"],
    ),
    BankEmail(
        email_id="E015",
        sender="suresh.menon@gmail.com",
        subject="Education loan disbursement delayed — semester starting soon",
        body=(
            "Hello Support,\n\nMy education loan (EL-2026-00123) was sanctioned a month ago "
            "but disbursement is still pending. My college semester fees are due in 5 days. "
            "Please expedite the disbursement urgently or I risk losing my admission.\n\nSuresh Menon"
        ),
        timestamp="2026-04-08T06:00:00Z",
        true_category=EmailCategory.LOAN_COMPLAINT,
        true_priority=Priority.HIGH,
        true_department=Department.LOANS,
        expected_keywords=["disburse", "expedite", "urgent", "sanction", "college"],
    ),

    # ── CARD_SERVICES (HIGH/MEDIUM → card_operations) ─────────────────────
    BankEmail(
        email_id="E016",
        sender="meera.pillai@gmail.com",
        subject="Block my debit card — it's been lost",
        body=(
            "Hello,\n\nI have lost my debit card (ending 9923) and need it blocked "
            "immediately to prevent misuse. Please also let me know how to get a "
            "replacement card. Is there a charge?\n\nMeera Pillai"
        ),
        timestamp="2026-04-08T08:00:00Z",
        true_category=EmailCategory.CARD_SERVICES,
        true_priority=Priority.HIGH,
        true_department=Department.CARD_OPERATIONS,
        expected_keywords=["block", "lost card", "replacement", "secure", "hotlist"],
    ),
    BankEmail(
        email_id="E017",
        sender="kiran.bhat@gmail.com",
        subject="Credit card bill not received — payment due soon",
        body=(
            "Hi,\n\nI haven't received my credit card statement for March 2026 "
            "(Card ending 7712). My payment due date is 12th April. Please send "
            "the statement immediately so I can pay without incurring late fees.\n\nKiran Bhat"
        ),
        timestamp="2026-04-08T09:45:00Z",
        true_category=EmailCategory.CARD_SERVICES,
        true_priority=Priority.MEDIUM,
        true_department=Department.CARD_OPERATIONS,
        expected_keywords=["statement", "bill", "due date", "send", "late fee"],
    ),
    BankEmail(
        email_id="E018",
        sender="tanya.gupta@gmail.com",
        subject="Request to increase credit card limit",
        body=(
            "Dear Bank,\n\nI have been a loyal customer for 5 years and always pay "
            "my credit card bill on time. I would like to request an increase in my "
            "credit limit from ₹1,50,000 to ₹3,00,000. Please let me know the process.\n\n"
            "Tanya Gupta, Card: XXXX5544"
        ),
        timestamp="2026-04-07T15:00:00Z",
        true_category=EmailCategory.CARD_SERVICES,
        true_priority=Priority.LOW,
        true_department=Department.CARD_OPERATIONS,
        expected_keywords=["limit", "increase", "credit", "eligibility", "apply"],
    ),
    BankEmail(
        email_id="E019",
        sender="rohit.saxena@outlook.com",
        subject="My card is not working for international transactions",
        body=(
            "Hello,\n\nI am traveling to Singapore next week and need to enable "
            "international usage on my credit card (ending 3312). Currently it gets "
            "declined for foreign transactions. How do I activate this?\n\nRohit Saxena"
        ),
        timestamp="2026-04-08T10:15:00Z",
        true_category=EmailCategory.CARD_SERVICES,
        true_priority=Priority.MEDIUM,
        true_department=Department.CARD_OPERATIONS,
        expected_keywords=["international", "enable", "activate", "abroad", "settings"],
    ),
    BankEmail(
        email_id="E020",
        sender="lalitha.krishna@gmail.com",
        subject="Reward points not credited after purchase",
        body=(
            "Hi,\n\nI made a purchase of ₹25,000 at an electronics store on 5th April "
            "using my rewards credit card (ending 6621) but the reward points have not "
            "been credited to my account. These should have been 2,500 points. "
            "Please investigate.\n\nLalitha Krishna"
        ),
        timestamp="2026-04-08T11:30:00Z",
        true_category=EmailCategory.CARD_SERVICES,
        true_priority=Priority.LOW,
        true_department=Department.CARD_OPERATIONS,
        expected_keywords=["reward points", "credit", "purchase", "investigate", "points"],
    ),

    # ── GENERAL_FEEDBACK (LOW → customer_care) ────────────────────────────
    BankEmail(
        email_id="E021",
        sender="anand.raj@gmail.com",
        subject="Mobile app is very slow and crashes often",
        body=(
            "Hello,\n\nYour mobile banking app has been extremely slow for the past week. "
            "It crashes when I try to view my statement or transfer money. "
            "Please fix this ASAP. Many of my friends have the same issue.\n\nAnand Raj"
        ),
        timestamp="2026-04-07T20:00:00Z",
        true_category=EmailCategory.GENERAL_FEEDBACK,
        true_priority=Priority.LOW,
        true_department=Department.CUSTOMER_CARE,
        expected_keywords=["app", "fix", "improve", "team", "apologize", "update"],
    ),
    BankEmail(
        email_id="E022",
        sender="divya.menon@gmail.com",
        subject="Branch staff was very rude and unhelpful",
        body=(
            "Dear Management,\n\nI visited your Andheri West branch on 7th April and "
            "the staff member at the counter was rude and dismissive when I asked for "
            "help with a fixed deposit. This is unacceptable. I am a 10-year customer.\n\n"
            "Divya Menon"
        ),
        timestamp="2026-04-08T07:45:00Z",
        true_category=EmailCategory.GENERAL_FEEDBACK,
        true_priority=Priority.LOW,
        true_department=Department.CUSTOMER_CARE,
        expected_keywords=["apologize", "staff", "feedback", "branch manager", "improve"],
    ),
    BankEmail(
        email_id="E023",
        sender="harish.nambiar@gmail.com",
        subject="Suggestion: Add UPI payment in mobile app",
        body=(
            "Hello,\n\nI love your bank's services but I wish your mobile app supported "
            "UPI payments directly. Currently I have to use a third-party app. "
            "Please consider adding this feature. It would make banking much easier.\n\nHarish"
        ),
        timestamp="2026-04-07T13:00:00Z",
        true_category=EmailCategory.GENERAL_FEEDBACK,
        true_priority=Priority.LOW,
        true_department=Department.CUSTOMER_CARE,
        expected_keywords=["thank", "suggestion", "UPI", "feature", "forward"],
    ),
    BankEmail(
        email_id="E024",
        sender="geeta.iyer@gmail.com",
        subject="Compliment for your customer service team",
        body=(
            "Dear Bank,\n\nI wanted to appreciate the excellent service I received "
            "from your phone banking team when resolving my account issue last week. "
            "The agent was patient and very helpful. Please pass on my compliments.\n\nGeeta Iyer"
        ),
        timestamp="2026-04-07T12:00:00Z",
        true_category=EmailCategory.GENERAL_FEEDBACK,
        true_priority=Priority.LOW,
        true_department=Department.CUSTOMER_CARE,
        expected_keywords=["thank", "appreciate", "share", "team", "positive"],
    ),
    BankEmail(
        email_id="E025",
        sender="sachin.pawar@gmail.com",
        subject="ATM near my home is always out of cash",
        body=(
            "Hello,\n\nThe ATM at MG Road, Pune (ATM ID: ATM-PUN-0021) is always out "
            "of cash on weekends. This is very inconvenient for people in the area. "
            "Please ensure it is replenished regularly, especially before weekends.\n\nSachin Pawar"
        ),
        timestamp="2026-04-07T17:00:00Z",
        true_category=EmailCategory.GENERAL_FEEDBACK,
        true_priority=Priority.LOW,
        true_department=Department.CUSTOMER_CARE,
        expected_keywords=["ATM", "replenish", "noted", "forward", "operations"],
    ),

    # ── UNRELATED (LOW → no_action) ───────────────────────────────────────
    BankEmail(
        email_id="E026",
        sender="spam123@randommail.com",
        subject="Win a free iPhone 16 — click here!",
        body=(
            "Congratulations! You've been selected to win a free iPhone 16. "
            "Click the link below to claim your prize immediately. Limited offer!\n\n"
            "http://totally-not-spam.com/claim"
        ),
        timestamp="2026-04-08T06:30:00Z",
        true_category=EmailCategory.UNRELATED,
        true_priority=Priority.LOW,
        true_department=Department.NO_ACTION,
        expected_keywords=["unrelated", "no action", "spam"],
    ),
    BankEmail(
        email_id="E027",
        sender="vendor.sales@officesupplies.com",
        subject="Special offer on office stationery — buy in bulk!",
        body=(
            "Dear Sir/Madam,\n\nWe are pleased to offer you bulk discounts on office "
            "stationery including pens, paper, and folders. Contact us for a quote.\n\n"
            "Best,\nOffice Supplies Co."
        ),
        timestamp="2026-04-07T10:00:00Z",
        true_category=EmailCategory.UNRELATED,
        true_priority=Priority.LOW,
        true_department=Department.NO_ACTION,
        expected_keywords=["unrelated", "no action", "vendor"],
    ),
    BankEmail(
        email_id="E028",
        sender="news.digest@newsletter.com",
        subject="Today's top business news — April 2026",
        body=(
            "Good morning! Here are today's top business headlines:\n"
            "- Sensex crosses 85,000\n"
            "- RBI holds rates steady\n"
            "- IT sector sees record hiring\n\n"
            "Unsubscribe: click here"
        ),
        timestamp="2026-04-08T06:00:00Z",
        true_category=EmailCategory.UNRELATED,
        true_priority=Priority.LOW,
        true_department=Department.NO_ACTION,
        expected_keywords=["unrelated", "no action", "newsletter"],
    ),
    BankEmail(
        email_id="E029",
        sender="job.seeker@email.com",
        subject="Applying for job at your bank — please review my CV",
        body=(
            "Dear HR,\n\nI am interested in working at your bank and have attached "
            "my CV for your review. I have 3 years of experience in banking operations.\n\n"
            "Regards,\nJob Seeker"
        ),
        timestamp="2026-04-07T09:00:00Z",
        true_category=EmailCategory.UNRELATED,
        true_priority=Priority.LOW,
        true_department=Department.NO_ACTION,
        expected_keywords=["unrelated", "HR", "no action", "redirect"],
    ),
    BankEmail(
        email_id="E030",
        sender="catering@eventco.in",
        subject="Catering services for your bank's annual event",
        body=(
            "Dear Events Team,\n\nWe provide premium catering services for corporate events. "
            "Please consider us for your upcoming annual function. We can accommodate "
            "up to 500 guests.\n\nEventCo Catering"
        ),
        timestamp="2026-04-07T11:30:00Z",
        true_category=EmailCategory.UNRELATED,
        true_priority=Priority.LOW,
        true_department=Department.NO_ACTION,
        expected_keywords=["unrelated", "no action", "vendor"],
    ),
]

# Index by email_id for fast lookup
EMAIL_INDEX: dict[str, BankEmail] = {e.email_id: e for e in BANK_EMAILS}