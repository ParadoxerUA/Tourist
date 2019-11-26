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

## Cron usage

> crontab -e
Insert the following code into opened file. Dont forget
to change PATH variable

#set PATH variable to your path to "tourist" folder 
#e.g my full path is "/home/rukadelica/tourist"
#there fore variable is set to "tourist"
PATH = tourist
59 */23 * * * $PATH/cron_task/sh-script tourist

save file and enjoy
