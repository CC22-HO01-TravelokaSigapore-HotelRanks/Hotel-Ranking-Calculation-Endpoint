FROM python:3.10.3-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update

RUN pip install -r requirements.txt

ENV HOST 0.0.0.0

EXPOSE 8001

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]