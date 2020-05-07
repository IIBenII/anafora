FROM python:3.8

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["uwsgi", "uwsgi.ini"]