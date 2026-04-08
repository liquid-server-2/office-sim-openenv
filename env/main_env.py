import json
from tasks.graders import email_grade, meeting_grade, doc_grade


class OfficeEnv:
    def __init__(self):
        self.tasks = [
            {"name": "email_triage", "grader": email_grade},
            {"name": "meeting_scheduler", "grader": meeting_grade},
            {"name": "document_review", "grader": doc_grade},
        ]

        self.current_task = 0
        self.done = False

        self.email_data = json.load(open("data/emails.json"))
        self.meeting_data = json.load(open("data/meetings.json"))
        self.doc_data = json.load(open("data/docs.json"))

    def get_tasks(self):
        return [t["name"] for t in self.tasks]

    async def reset(self):
        self.current_task = 0
        self.done = False

        return type("Res", (), {
            "observation": {
                "task": "email_triage",
                "content": self.email_data[0]["text"]
            },
            "done": False
        })

    async def step(self, action):
        task_name = self.tasks[self.current_task]["name"]

        if task_name == "email_triage":
            expected = self.email_data[0]["label"]
            reward = email_grade(action, expected)
            next_obs = {
                "task": "meeting_scheduler",
                "content": self.meeting_data[0]["request"]
            }

        elif task_name == "meeting_scheduler":
            expected = self.meeting_data[0]["valid"]
            reward = meeting_grade(action, expected)
            next_obs = {
                "task": "document_review",
                "content": self.doc_data[0]["text"]
            }

        else:
            expected = self.doc_data[0]["risk"]
            reward = doc_grade(action, expected)
            self.done = True
            next_obs = {
                "task": "done",
                "content": "completed"
            }

        self.current_task += 1

        return type("Res", (), {
            "observation": next_obs,
            "reward": reward,
            "done": self.done
        })

    async def close(self):
        pass