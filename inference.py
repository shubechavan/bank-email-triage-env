import os
import asyncio
import json
import httpx
from typing import List, Dict, Any
from openai import AsyncOpenAI

def log_start(task: str, env: str, model: str):
    print(f"[START] {json.dumps({'task': task, 'benchmark': env, 'model': model})}")

def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    print(f"[STEP] {json.dumps({'step': step, 'action': action, 'reward': reward, 'done': done, 'error': error})}")

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    print(f"[END] {json.dumps({'success': success, 'steps': steps, 'score': score, 'rewards': rewards})}")

async def get_model_message(client: AsyncOpenAI, model_name: str, task_id: str, obs_text: str) -> str:
    # Build prompt based on task
    system_prompt = "You are a bank email triage AI. Respond with JSON based on the exact task instructions."
    
    if task_id == "task_1":
        content = f"Categorize this email.\nEmail:\n{obs_text}\nReturn JSON with key 'category'. Categories: fraud_dispute, account_inquiry, loan_complaint, card_services, general_feedback, unrelated"
    elif task_id == "task_2":
        content = f"Categorize, prioritize, and route.\nEmail:\n{obs_text}\nReturn JSON with keys: 'category', 'priority', 'department'."
    else:
        content = f"Categorize, prioritize, route, and draft response.\nEmail:\n{obs_text}\nReturn JSON with keys: 'category', 'priority', 'department', 'response_draft'."

    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[DEBUG] OpenAI client error: {e}")
        # fallback
        return json.dumps({"category": "general_feedback", "priority": "low", "department": "customer_care", "response_draft": "We will look into this."})

async def run_task(task_id: str, env_url: str, client: AsyncOpenAI, model_name: str):
    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    
    # 1. Start Log
    log_start(task=task_id, env="BankEmailTriage-v1", model=model_name)
    
    try:
        # Reset Environment
        async with httpx.AsyncClient() as http_client:
            reset_resp = await http_client.post(f"{env_url}/reset", json={"task_id": task_id})
            reset_data = reset_resp.json()
            obs = reset_data["observation"]
            done = reset_data["done"]
        
        last_echoed = obs.get("echoed_message", "")
        last_reward = 0.0
        MAX_STEPS = 1
        
        for step in range(1, MAX_STEPS + 1):
            if done:
                break
            
            # Context for model
            obs_text = f"Subject: {obs['subject']}\nBody: {obs['body']}"
            
            # Predict
            message = await get_model_message(client, model_name, task_id, obs_text)
            
            try:
                action_data = json.loads(message)
            except:
                action_data = {"category": "general_feedback"}
                
            # Submit action
            payload = {"action": action_data}
            async with httpx.AsyncClient() as http_client:
                step_resp = await http_client.post(f"{env_url}/step", json=payload)
                step_data = step_resp.json()
            
            obs = step_data["observation"]
            reward = step_data["reward"]
            done = step_data["done"]
            error = None
            
            rewards.append(reward)
            steps_taken = step
            last_echoed = obs.get("echoed_message", "")
            last_reward = reward
            
            log_step(step=step, action=message, reward=reward, done=done, error=error)
            history.append(f"Step {step}: {message!r} -> reward {reward:+.2f}")
            
            if done:
                break
                
        # Calculate final score
        # Since it's 1 step per episode, score is just the reward.
        score = sum(rewards)
        score = min(max(score, 0.0), 1.0)
        
        # Success thresholds defined in openenv.yaml
        thresholds = {"task_1": 0.95, "task_2": 0.8, "task_3": 0.7}
        success = score >= thresholds.get(task_id, 0.5)

    except Exception as e:
        print(f"[DEBUG] Error running step: {e}")
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

async def main():
    # LLM Config
    # If API_BASE_URL is set, it's used for LLM. If not, use generic together/openai
    llm_api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    hf_token = os.getenv("HF_TOKEN")
    
    # Init OpenAI client routing it to API_BASE_URL with the HF_TOKEN as api_key
    client = AsyncOpenAI(
        api_key=hf_token,
        base_url=llm_api_base
    )
    
    # Environment Local URL
    # Hardcoded or passed, usually the FastApi runs on port 7860
    env_url = os.getenv("ENV_URL", "http://127.0.0.1:7860")
    
    for task in ["task_1", "task_2", "task_3"]:
        await run_task(task, env_url, client, model_name)

if __name__ == "__main__":
    asyncio.run(main())
