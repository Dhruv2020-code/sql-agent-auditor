from openai import OpenAI
import os
import requests

def run_evaluation():
    
    api_base = os.environ.get("API_BASE_URL")
    
    
    api_key = os.environ.get("HF_TOKEN") or os.environ.get("API_KEY")
    model_name = os.environ.get("MODEL_NAME")

    client = OpenAI(
        base_url=api_base,
        api_key=api_key
    )

    print(f"[START] task=sql_audit model={model_name}")

    try:
        
        url = "http://127.0.0.1:7860"

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Return ONLY the SQL function name to sum a column. No extra text."},
                {"role": "user", "content": "What is the sum of total_amount?"}
            ]
        )
        
        
        action_str = completion.choices[0].message.content.strip()

       
        response = requests.post(
            f"{url}/step",
            json={"query": f"SELECT {action_str} FROM orders"}
        ).json()

        reward = float(response.get("reward", 0.0))
        done = str(response.get("done", True)).lower()

        
        print(f"[STEP] step=1 action={action_str} reward={reward:.2f} done={done} error=null")
        print(f"[END] success=true steps=1 rewards={reward:.2f}")

    except Exception as e:
        print(f"[END] success=false steps=0 rewards=0.00 error={str(e)}")

if __name__ == "__main__":
    run_evaluation()
