import subprocess
import time
import requests


def start_server():
    return subprocess.Popen(["python", "main.py"])


def wait_for_server():
    url = "http://127.0.0.1:7860/reset"
    for _ in range(30):
        try:
            r = requests.post(url, timeout=2)
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(2)
    return False


def run():
    server = start_server()

    if not wait_for_server():
        print("Server failed to start")
        server.kill()
        return

    subprocess.run(["python", "inference.py"])
    server.kill()


if __name__ == "__main__":
    run()