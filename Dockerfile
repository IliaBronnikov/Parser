FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD uvicorn parser:app --host 0.0.0.0 --port 8000
