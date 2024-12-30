FROM python:3.13

RUN pip install poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY discord_bot/ discord_bot/

CMD ["poetry", "run", "python", "-m", "discord_bot.main"]
