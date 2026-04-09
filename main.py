from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import uvicorn
import os

app = FastAPI()

class Action(BaseModel):
    query: str

class Observation(BaseModel):
    observation: str
    reward: float
    done: bool

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.post("/reset")
def reset():
    return {"observation": "Environment reset successful.", "reward": 0.0, "done": False}

@app.get("/state")
def state():
    return {"observation": "Tables: users, products, orders. Task: Get total orders sum."}

@app.post("/step", response_model=Observation)
def step(action: Action):
    db_path = "data.db"
    if not os.path.exists(db_path):
        return Observation(observation="Error: data.db not found", reward=0.0, done=True)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(action.query, conn)
        # Clean string output for the validator
        result = df.to_string(index=False)
        return Observation(observation=result, reward=1.0, done=True)
    except Exception as e:
        return Observation(observation=str(e), reward=-0.1, done=False)
    finally:
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
