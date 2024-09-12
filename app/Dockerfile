FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y docker.io

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
