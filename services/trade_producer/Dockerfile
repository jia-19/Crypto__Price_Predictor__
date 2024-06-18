FROM python:3.10.3-slim-buster

ENV PYTHONUNBUFFERED=1

RUN pip install poetry==1.8.3

WORKDIR /app

# Copy pyproject.toml and poetry.lock files into container
COPY pyproject.toml poetry.lock /app/

#install dependencies
RUN poetry install

# Copy all src code into container
COPY . /app

CMD ["poetry", "run", "python", "src/main.py"]