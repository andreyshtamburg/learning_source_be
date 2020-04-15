FROM python:3.7.6

# Flask config
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

# Python config to run flask app in container
ENV PYTHONUNBUFFERED 1

WORKDIR /learning_source

COPY app app/
COPY Pip* ./
COPY *.py ./

RUN pip install --upgrade pip && pip install pipenv && pipenv install --dev --system --deploy --ignore-pipfile

CMD python main.py run
