FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip zip

WORKDIR /app

COPY . .

RUN pip3 install fastapi uvicorn pymongo requests

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]