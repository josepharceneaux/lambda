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

# Deploy this Lambda function to AWS
deploy: install
install: env
	../scripts/deploy_lambda.py --deploy --function ${FUNCTION}

clean:
	rm -rf tests/__pycache__

distclean:
	rm -rf deployments/deployment_* /tmp/

deactivate:
	$(shell deactivate)


# Bucket actions
list-buckets:
	./scanBuckets.py list
scan-buckets:
	./scanBuckets.py scan
bucket-logging:
	./scanBuckets.py logging
fix-buckets:
	./scanBuckets.py modify
bucket-encryption:
	./scanBuckets.py encryption


test: tests
tests: env
	pytest tests
