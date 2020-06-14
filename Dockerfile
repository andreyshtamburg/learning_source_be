FROM python:3.8

LABEL Author="Andrei Shtamburg"
LABEL E-mail="andrewshtamburg@gmail.com"
LABEL version="0.0.1b"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "main.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

RUN mkdir /ls
WORKDIR /ls

COPY Pip* /ls/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile

ADD . /ls

EXPOSE 4433

CMD flask run --host=0.0.0.0 --port=4433
