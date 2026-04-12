from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from sql import run_query

app = FastAPI()

DB_PATH = os.path.join(os.getcwd(), "data.db")


def init_db():
    print("Files:", os.listdir())

    if not os.path.exists(DB_PATH):
        print("data.db not found, creating fallback DB")

        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            total_amount REAL
        )
        """)

        cursor.executemany(
            "INSERT INTO orders (total_amount) VALUES (?)",
            [(100,), (200,), (300,)]
        )

        conn.commit()
        conn.close()
    else:
        print("Using existing data.db")


init_db()


class Action(BaseModel):
    query: str


class Observation(BaseModel):
    observation: str
    reward: float
    done: bool


@app.get("/")
def root():
    return {"message": "Server running"}


@app.post("/reset", response_model=Observation)
def reset():
    return Observation(observation="Reset successful", reward=0.95, done=False)


@app.post("/step", response_model=Observation)
def step(action: Action):
    result = run_query(action.query)

    if isinstance(result, str):
        return Observation(observation=result, reward=0.95, done=True)

    if result.empty:
        result_str = "No results found"
    else:
        result_str = result.to_string(index=False)

    return Observation(observation=result_str, reward=0.95, done=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

