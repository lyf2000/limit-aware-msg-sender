FROM python:3.12.3-bookworm

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1


RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev
COPY reqs.txt .
RUN pip install -r reqs.txt


WORKDIR /app
COPY . .

CMD ["python", "/app/consumer/main.py"]