FROM python:3.8

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /auth_service/

WORKDIR /auth_service/

COPY ./src/ /auth_service/