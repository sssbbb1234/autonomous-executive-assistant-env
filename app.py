from fastapi import FastAPI
from env import ExecutiveAssistantEnv

app = FastAPI()

env = None


@app.get("/")
def home():
    return {"message": "Executive Assistant Environment Running"}


@app.post("/reset")
def reset():
    global env
    env = ExecutiveAssistantEnv(difficulty="easy")
    obs = env.reset()
    return obs.model_dump()


@app.post("/step")
def step(action: dict):
    global env
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }