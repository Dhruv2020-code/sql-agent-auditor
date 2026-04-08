from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import uvicorn

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

@app.get("/state")
def state():
    return {"observation": "Tables: users, products, orders. Task: Get total orders."}

@app.post("/step", response_model=Observation)
def step(action: Action):
    conn = sqlite3.connect("data.db")
    try:
        df = pd.read_sql_query(action.query, conn)
        result = df.to_string()
        return Observation(observation=result, reward=1.0, done=True)
    except Exception as e:
        return Observation(observation=str(e), reward=-0.1, done=False)
    finally:
        conn.close()

# Is block ko dhayan se dekhein
def start():
    import uvicorn
    # Port 7860 hi rehne dena kyunki Hugging Face wahi use karta hai
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    start()
