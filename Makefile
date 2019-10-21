SHELL := /bin/bash
debug:
	python3 -m venv venv
	source ./venv/bin/activate && \
	if ! apt list --installed | grep redis-server; \
	then sudo apt install redis-server; \
	fi && \
	if ! pgrep redis-server;\
	then /etc/init.d/redis-server start;\
	fi && \
	pip3 install -r ./requirements/test_requirements.txt && \
	cd ./api && gunicorn --bind 127.0.0.1:5000 wsgi:app && \
	/etc/init.d/redis-server stop

run_tests:
	python3 -m venv venv
	source ./venv/bin/activate && \
	if ! apt list --installed | grep redis-server; \
	then sudo apt install redis-server; \
	fi && \
	if ! pgrep redis-server;\
	then /etc/init.d/redis-server start;\
	fi && \
	pip3 install -r ./requirements/test_requirements.txt && \
	python -m unittest discover -s ./tests/unittests && \
	/etc/init.d/redis-server stop
