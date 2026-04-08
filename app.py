from fastapi import FastAPI
from env import ExecutiveAssistantEnv
from models import Action

app = FastAPI()
env = None


def main():
    return app


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    global env
    env = ExecutiveAssistantEnv(difficulty="easy")
    obs = env.reset()
    return obs.model_dump()


@app.post("/step")
def step(action: dict):
    global env

    if env is None:
        return {"error": "Call /reset first"}

    try:
        action_obj = Action(**action)
    except Exception as e:
        return {"error": str(e)}

    obs, reward, done, info = env.step(action_obj)

    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }