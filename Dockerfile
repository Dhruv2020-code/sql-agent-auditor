FROM python:3.10

# Hugging Face permissions fix
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

# Dependencies install karein
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Pura code copy karein
COPY --chown=user . .

# Port expose karein (Hugging Face standard)
EXPOSE 7860

CMD ["sh", "-c", "python main.py & sleep 10 && python inference.py || echo 'INFERENCE CRASHED'"]
