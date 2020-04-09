FROM python:3.8

COPY /requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# COPY /BqManager.py /BqManager.py
WORKDIR /app

ENTRYPOINT ["rq", "worker", "-u"]