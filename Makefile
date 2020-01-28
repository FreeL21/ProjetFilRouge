all: start

env:
	. ./venv/bin/activate

start:
	python3 ./src/services.py
