from fastapi import FastAPI
from pydantic import BaseModel
from env.main_env import OfficeEnv
import asyncio

app = FastAPI()

env = OfficeEnv()


class Action(BaseModel):
    message: str


@app.post("/reset")
async def reset():
    result = await env.reset()
    return {
        "observation": result.observation,
        "done": result.done
    }


@app.post("/step")
async def step(action: Action):
    result = await env.step(action.message)
    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done
    }


@app.get("/state")
async def state():
    return {"status": "running"}