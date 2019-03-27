PIP=pip3

env: requirements.txt
	source ~/.pyenv/lambda-tools/bin/activate
	${PIP} install -r requirements.txt

build:
	../scripts/deploy_lambda.py --build

install:
	../scripts/deploy_lambda.py --deploy
