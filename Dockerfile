FROM python:3

WORKDIR /code

ENV PYTHONPATH /code

COPY . /code

RUN python -m pip install -r ./requirements.txt

## https://github.com/heroku/cli/issues/1081
# ENTRYPOINT ["./scripts/bot"]
CMD ["./scripts/bot"]

# CMD ["bot.py"]