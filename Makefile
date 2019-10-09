SHELL := /bin/bash
debug:
	python3 -m venv venv
	source ./venv/bin/activate && \
	pip3 install -r ./requirements/test_requirements.txt && \
	cd ./api && gunicorn --bind 127.0.0.1:5000 wsgi:app

run_tests:
	python3 -m venv venv
	source ./venv/bin/activate && \
	pip3 install -r ./requirements/test_requirements.txt && \
	python -m unittest discover -s ./tests/unittests
