FROM python:3.9

WORKDIR /app
COPY . .

RUN rm -f poetry.lock; pip install poetry locust && poetry install 

ENTRYPOINT ["poetry", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0"]