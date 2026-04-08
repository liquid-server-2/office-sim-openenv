from fastapi import FastAPI
from pydantic import BaseModel
from env.main_env import OfficeEnv
import uvicorn

app = FastAPI()
env = OfficeEnv()


# -------- ACTION MODEL --------
class Action(BaseModel):
    message: str


# -------- RESET --------
@app.post("/reset")
async def reset():
    result = await env.reset()
    return {
        "observation": result.observation,
        "done": result.done
    }


# -------- STEP --------
@app.post("/step")
async def step(action: Action):
    result = await env.step(action.message)
    return {
        "observation": result.observation,
        "reward": result.reward,
        "done": result.done
    }


# -------- STATE --------
@app.get("/state")
async def state():
    return {"status": "running"}


# ✅ CRITICAL: TASK DISCOVERY ENDPOINT
@app.get("/tasks")
async def get_tasks():
    return {
        "tasks": [
            {
                "name": "email_triage",
                "grader": "tasks.graders.email_grade"
            },
            {
                "name": "meeting_scheduler",
                "grader": "tasks.graders.meeting_grade"
            },
            {
                "name": "document_review",
                "grader": "tasks.graders.doc_grade"
            }
        ]
    }


# -------- ROOT (optional, removes 404) --------
@app.get("/")
def home():
    return {"message": "OfficeSim OpenEnv API running"}


# -------- REQUIRED MAIN FUNCTION --------
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# -------- ENTRYPOINT --------
if __name__ == "__main__":
    main()