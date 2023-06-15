FROM python:3.10-slim

WORKDIR /encodec

COPY ./requirements.txt /encodec/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /encodec/requirements.txt

COPY ./app /encodec/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]