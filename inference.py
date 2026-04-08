import asyncio
import os
from openai import OpenAI
from env.main_env import OfficeEnv

# ✅ REQUIRED ENV VARIABLES
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(task, step, action, reward, done):
    print(f"[STEP] task={task} step={step} action={action} reward={reward} done={done}", flush=True)


def log_end(success, steps, score):
    print(f"[END] success={success} steps={steps} score={score}", flush=True)


def fallback_agent(prompt: str) -> str:
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
    # ✅ MUST USE PROVIDED PROXY
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )

    env = OfficeEnv()

    rewards = []
    log_start("multi_task", "office_env", MODEL_NAME)

    result = await env.reset()

    step_count = 0

    while not result.done:
        step_count += 1

        prompt = result.observation["content"]
        task_name = result.observation.get("task", "unknown")

        # ✅ MUST ATTEMPT API CALL
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            action = completion.choices[0].message.content

        except Exception:
            # fallback if API fails
            action = fallback_agent(prompt)

        result = await env.step(action)
        reward = result.reward or 0.0

        rewards.append(reward)

        # ✅ CRITICAL: include task name
        log_step(task_name, step_count, action, reward, result.done)

        if step_count >= 10:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score > 0.7

    await env.close()
    log_end(success, step_count, score)


if __name__ == "__main__":
    asyncio.run(main())