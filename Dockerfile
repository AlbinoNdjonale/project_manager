FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /app

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip install poetry
RUN poetry install

COPY . .

EXPOSE 8000/tcp

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]