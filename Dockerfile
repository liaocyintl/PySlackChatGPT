FROM python:3.10

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code

CMD ["python", "main.py"]