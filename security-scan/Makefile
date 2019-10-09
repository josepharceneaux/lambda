#! /bin/bash

SHELL=/bin/bash
PIP=pip3
PYENV=~/.pyenv/lambda-tools/bin/activate
FUNCTION := $(shell basename $(PWD))


venv: env
env: requirements.txt
	${PYENV}
	${PIP} install -r requirements.txt

build: env
	echo "Building ${FUNCTION}"
	../scripts/deploy_lambda.py --build --function ${FUNCTION}

deploy: install
install: env
	../scripts/deploy_lambda.py --deploy --function ${FUNCTION}

clean:
	$(shell deactivate)


test: tests
tests: env
	pytest
