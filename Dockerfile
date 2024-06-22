FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    firefox-esr \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY drivers/geckodriver /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver

WORKDIR /docker_hw

COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY .. .

CMD ["pytest"]
