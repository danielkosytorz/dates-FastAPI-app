FROM python:3.10
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update -q && apt-get install -yq netcat
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["sh", "./wait_for_database.sh"]