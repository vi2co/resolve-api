FROM python:slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY app.py config.py /app/
RUN apt-get update && apt-get -y install libpq-dev python-dev gcc && \
    pip install Flask dnspython werkzeug sqlalchemy prometheus-flask-exporter psycopg2

EXPOSE 3000

CMD ["flask", "run", "-p", "3000"]
