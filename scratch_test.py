import httpx
import asyncio
import json

async def test():
    async with httpx.AsyncClient() as c:
        for cat in ["fraud_dispute", "account_inquiry", "loan_complaint", "card_services", "general_feedback", "unrelated"]:
            r1 = await c.post('http://127.0.0.1:7860/reset', json={'task_id':'task_1'})
            obs = r1.json()['observation']
            r2 = await c.post('http://127.0.0.1:7860/step', json={'action':{'category': cat}})
            # print answer
            print(f"Cat {cat} -> reward is {r2.json()['reward']}")

if __name__ == '__main__':
    asyncio.run(test())
