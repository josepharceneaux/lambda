PENV_DIR=~/.pyenv
PIP=pip3
DEPLOYMENTS_DIR=deployments

# Initialize our Python environment, create deployments directory
init:
	source ${PENV_DIR}/lambda-tools/bin/activate
	${PIP} install -r requirements.txt
	test -d ${DEPLOYMENTS_DIR} || mkdir ${DEPLOYMENTS_DIR}

test:
	@echo ${PENV_DIR}/lambda-tools/bin/activate
