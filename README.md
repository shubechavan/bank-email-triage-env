---
title: Bank Email Triage Env
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# Bank Email Triage Environment

OpenEnv-compliant environment for training AI agents on bank customer support email triage. The environment is evaluated using three progressive tasks:
1. Categorization
2. Categorization + Priority + Routing
3. Full Response Generation

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python -m app.main
```

3. Run inference test:
```bash
# Don't forget to set TOGETHER_API_KEY in .env
python inference.py
```

## Space Deployment
This project is configured for deployment on Hugging Face Spaces using the Docker SDK.
1. Create a new Space with Docker.
2. Push all files.
3. Configure Space secrets: `HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`, etc.
