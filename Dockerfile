# 1. Base image: Python 3.10 use kar rahe hain jo stable hai
FROM python:3.10

# 2. Working directory set karein (Hugging Face par isi folder mein code rahega)
WORKDIR /code

# 3. Pehle requirements copy karein taaki libraries install ho sakein
COPY ./requirements.txt /code/requirements.txt

# 4. Saari libraries install karein
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Apna saara local code (main.py, data.db, etc.) container mein copy karein
COPY . .

# 6. Server start karne ki command. 
# Hugging Face default mein port 7860 use karta hai, isliye hum wahi set kar rahe hain.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]