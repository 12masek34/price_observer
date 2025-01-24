ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as python-base

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD alembic upgrade head && python main.py
