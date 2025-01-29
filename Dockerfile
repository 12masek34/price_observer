ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as python-base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    build-essential \
    xvfb \
    x11-utils \
    chromium \
    chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /root/.cache/*

ENV PATH="/usr/lib/chromium/:${PATH}"

CMD alembic upgrade head && rm -f /tmp/.X99-lock && Xvfb :99 -screen 0 1920x1080x24 & DISPLAY=:99 python main.py
