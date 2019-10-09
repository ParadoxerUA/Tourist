debug:
	python3 -m venv venv
	. ./venv/bin/activate
	./venv/bin/pip install -r ./requirements/test_requirements.txt
	cd ./api && gunicorn --bind 127.0.0.1:5000 wsgi:app

run_tests:
	python3 -m venv venv
	. ./venv/bin/activate
	./venv/bin/pip install -r ./requirements/test_requirements.txt
	python -m unittest discover -s ./tests/unittests
