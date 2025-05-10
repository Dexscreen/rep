FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install flask

CMD ["python", "chargeback_rpc.py"]
