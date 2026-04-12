from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from sql import run_query

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

print("Using DB at:", DB_PATH)


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
    return Observation(observation="Reset successful", reward=0, done=False)


@app.post("/step", response_model=Observation)
def step(action: Action):
    result = run_query(action.query)

    # error case
    if isinstance(result, str):
        return Observation(observation=result, reward=0, done=True)

    if result.empty:
        return Observation(observation="No results found", reward=0, done=True)

    result_str = result.to_string(index=False)

    reward = 0
    query_lower = action.query.lower()

    try:
        # EASY: count orders
        if "count" in query_lower:
            correct = run_query("SELECT COUNT(*) FROM orders")
            if (result.values == correct.values).all():
                reward = 1

        # MEDIUM: total revenue
        elif "sum" in query_lower:
            correct = run_query("SELECT SUM(total_amount) FROM orders")
            if (result.values == correct.values).all():
                reward = 1

        # HARD: top user by spending (FIXED)
        elif "group by" in query_lower:
            correct = run_query("""
                SELECT user_id, SUM(total_amount) as total
                FROM orders
                GROUP BY user_id
                ORDER BY total DESC
                LIMIT 1
            """)

            if result.shape == correct.shape:
                if (result.values.astype(float) == correct.values.astype(float)).all():
                    reward = 1

    except Exception:
        reward = 0

    return Observation(
        observation=result_str,
        reward=reward,
        done=True
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
