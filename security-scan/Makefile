PIP=pip3
PYENV="~/.pyenv/lambda-tools/bin/activate"

venv: env
env: requirements.txt
	source ${PYENV}
	${PIP} install -r requirements.txt

build: env
	../scripts/deploy_lambda.py --build --function security-scan

install: env
	../scripts/deploy_lambda.py --deploy --function security-scan

test: tests
tests: env
