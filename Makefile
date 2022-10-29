run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations && timeout 2 && python manage.py migrate

lint:
	poetry run isort survey_app
	poetry run black --exclude="survey_app/migrations/*" survey_app
	poetry run pylint --ignore-paths="survey_app/migrations/*" survey_app

req:
	poetry export -f requirements.txt --without-hashes --with dev --output requirements.txt
