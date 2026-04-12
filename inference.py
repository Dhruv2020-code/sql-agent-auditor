import os
import requests
import time
import sys
from openai import OpenAI

sys.stdout.reconfigure(line_buffering=True)

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN") or "dummy_key"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


def wait_for_server():
    url = "http://127.0.0.1:7860/reset"

    for i in range(30):
        try:
            r = requests.post(url, timeout=2)
            if r.status_code == 200:
                print("Server ready")
                return True
        except:
            pass
        time.sleep(2)

    return False


def run_task(task_id, question, fallback_sql):
    print(f"[START] {task_id}")

    url = "http://127.0.0.1:7860/step"

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"SQL for: {question}"}],
            timeout=30
        )
        action_str = completion.choices[0].message.content.strip()
    except:
        action_str = fallback_sql
    
    action_clean = action_str.strip().lower()

    if action_clean.startswith("select"):
        query = action_str
    elif "group by" in action_clean or "limit" in action_clean:
        query = f"SELECT {action_str}"
    else:
        query = f"SELECT {action_str} FROM orders"

    payload = {"query": query}

    try:
        r = requests.post(url, json=payload, timeout=5)
        print("Server response:", r.json())
    except Exception as e:
        print("Request failed:", str(e))

    print(f"[END] task={task_id}")


def main():
    if not wait_for_server():
        print("Server failed to start")
        return

    tasks = [
        ("task_1", "Count total orders", "COUNT(*)"),
        ("task_2", "Total revenue", "SUM(total_amount)"),
        ("task_3", "Top customer by spending",
         "customer_id, SUM(total_amount) as total FROM orders GROUP BY customer_id ORDER BY total DESC LIMIT 1")
    ]

    for t in tasks:
        run_task(*t)
        time.sleep(2)

    print("Finished all tasks")

    # keep container alive (HF requirement)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
