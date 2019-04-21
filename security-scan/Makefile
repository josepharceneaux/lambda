PIP=pip3

venv: env
env: requirements.txt
	source ~/.pyenv/lambda-tools/bin/activate
	${PIP} install -r requirements.txt

build: env
	../scripts/deploy_lambda.py --build

install: env
	../scripts/deploy_lambda.py --deploy

test: tests
tests: env
