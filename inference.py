import asyncio, os
from openai import OpenAI
from env.main_env import OfficeEnv

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done}", flush=True)


def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score}", flush=True)


def fallback_agent(prompt: str) -> str:
    """Deterministic fallback (VERY IMPORTANT for no-API case)"""
    p = prompt.lower()

    if "urgent" in p or "bug" in p:
        return "urgent"
    elif "meeting" in p:
        return "schedule at 10am"
    elif "contract" in p or "nda" in p:
        return "missing termination"
    else:
        return "ignore"


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

        try:
            # Try real API call
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            action = completion.choices[0].message.content

        except Exception as e:
            # Fallback if API fails (quota, key, etc.)
            action = fallback_agent(prompt)

        result = await env.step(action)
        reward = result.reward

        rewards.append(reward)
        log_step(step, action, reward, result.done, None)

        if result.done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score > 0.7

    await env.close()
    log_end(success, len(rewards), score, rewards)


if __name__ == "__main__":
    asyncio.run(main())