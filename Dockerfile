FROM python:3.6

ADD . /srv
WORKDIR /srv

RUN pip3 install gunicorn==19.9.0 && \
    pip3 install pipenv==2018.11.26 && \
    pip3 install psycopg2==2.8.3 && \
    pipenv install --deploy --system

EXPOSE 8000
