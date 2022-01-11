FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	python-is-python3 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ratp_api.py .

COPY ratp_app.py .

COPY requirements.txt .

COPY Wsiv.wsdl .

RUN pip install -r requirements.txt

ENTRYPOINT [ "uvicorn", "ratp_app:app", "--host", "0.0.0.0", "--port", "5000" ]
