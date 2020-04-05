# learning_source_be
Learning source back end

Run app with `FLASK_APP=$PWD/main.py FLASK_ENV=development pipenv run python -m flask run --port 4433`

For swagger doc access `http://localhost:4433/api/v1/doc/`

Start db on 5432 port `psql -d "host=localhost port=5432 dbname=source user=source"`
