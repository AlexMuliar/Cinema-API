FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY entrypoint.sh .
RUN pip install  -r requirements.txt 
# --no-cache-dir
COPY . .

# RUN pip install --upgrade pip && pip install -r ./app/requirements.txt

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]