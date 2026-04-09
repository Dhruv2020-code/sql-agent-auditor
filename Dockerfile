FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .

# Server ko background mein chalao, 5 second ruko, phir inference chalao
CMD sh -c "python main.py & sleep 5 && python inference.py"
