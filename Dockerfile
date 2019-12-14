FROM python:3

WORKDIR /code

ENV PYTHONPATH /code

COPY . /code

RUN python -m pip install -r ./requirements.txt

ENTRYPOINT ["./scripts/bot"]
# CMD ["bot.py"]