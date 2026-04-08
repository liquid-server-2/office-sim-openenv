import json
from tasks.graders import email_grade, meeting_grade, doc_grade

class OfficeEnv:
    def __init__(self):
        self.tasks = ["email", "meeting", "doc"]
        self.current_task = 0
        self.done = False

        self.email_data = json.load(open("data/emails.json"))
        self.meeting_data = json.load(open("data/meetings.json"))
        self.doc_data = json.load(open("data/docs.json"))

    async def reset(self):
        self.current_task = 0
        self.done = False

        return type("Res", (), {
            "observation": {
                "task": "email",
                "content": self.email_data[0]["text"]
            },
            "done": False
        })

    async def step(self, action):
        task = self.tasks[self.current_task]

        if task == "email":
            expected = self.email_data[0]["label"]
            reward = email_grade(action, expected)
            next_obs = {
                "task": "meeting",
                "content": self.meeting_data[0]["request"]
            }

        elif task == "meeting":
            expected = self.meeting_data[0]["valid"]
            reward = meeting_grade(action, expected)
            next_obs = {
                "task": "doc",
                "content": self.doc_data[0]["text"]
            }

        else:  # doc
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