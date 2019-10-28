# Tourist

## Usage

Run app in debug mode, run in console
> cd tourist

> make debug

Run tests, type in console
> cd tourist

> make run_tests 

## Test

Run in console
> make debug

> curl -GET localhost:5000/api/smoke/v1/smoke


## Migrations 

from tourist/api run:

> python manage.py db init

> python manage.py db migrate

> python manage.py db upgrade

## Celery usage

Start redis
> sudo service redis-server start

Run in console from tourist/celery_service with active venv
> celery worker -A app.app --loglevel=debug

