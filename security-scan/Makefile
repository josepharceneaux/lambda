PIP=pip3
PYENV="~/.pyenv/lambda-tools/bin/activate"
FUNCTION := $(shell basename $(PWD))


venv: env
env: requirements.txt
	source ${PYENV}
	${PIP} install -r requirements.txt

build: env
	../scripts/deploy_lambda.py --build --function ${FUNCTION}

install: env
	../scripts/deploy_lambda.py --deploy --function ${FUNCTION}

test: tests
tests: env
