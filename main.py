from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import uvicorn
import os

app = FastAPI()

def safe_score(score):
    return max(0.0001, min(score, 0.9999))

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
    
    return {
        "observation": "Environment reset successful.",
        "reward": safe_score(0.01),
        "done": False
    }

@app.get("/state")
def state():
    return {
        "observation": "Tables: users, products, orders. Tasks: 1. Sum total_amount, 2. Average price, 3. Count orders.",
        "tasks": ["sum_orders", "avg_price", "count_users"]
    }

@app.post("/step", response_model=Observation)
def step(action: Action):
    db_path = "data.db"

    if not os.path.exists(db_path):
        return Observation(
            observation="Error: data.db not found",
            reward=safe_score(0.1),
            done=True
        )

    conn = sqlite3.connect(db_path)
    try:
        query_upper = action.query.upper()

        df = pd.read_sql_query(action.query, conn)
        result = df.to_string(index=False)

       
        if any(x in query_upper for x in ["SUM", "AVG", "COUNT", "SELECT"]):
            reward = 0.85
        else:
            reward = 0.15

        reward = safe_score(reward)

        return Observation(
            observation=result,
            reward=reward,
            done=True
        )

    except Exception as e:
       
        return Observation(
            observation=str(e),
            reward=safe_score(0.01),
            done=False
        )

    finally:
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
