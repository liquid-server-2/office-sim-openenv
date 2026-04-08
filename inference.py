
import asyncio, os
from openai import OpenAI
from env.main_env import OfficeEnv

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done}", flush=True)

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score}", flush=True)

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = OfficeEnv()

    rewards = []
    log_start("multi_task", "office_env", MODEL_NAME)

    result = await env.reset()

    for step in range(1, 10):
        if result.done:
            break

        prompt = result.observation["content"]

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}]
        )

        action = completion.choices[0].message.content

        result = await env.step(action)
        reward = result.reward

        rewards.append(reward)
        log_step(step, action, reward, result.done, None)

        if result.done:
            break

    score = sum(rewards)/len(rewards)
    success = score > 0.7

    await env.close()
    log_end(success, len(rewards), score, rewards)

if __name__ == "__main__":
    asyncio.run(main())
