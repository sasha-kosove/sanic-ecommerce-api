FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get -y install netcat \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./entrypoint.sh .
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]