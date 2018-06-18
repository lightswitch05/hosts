PIP = 'pip3'
PYTEST = 'pytest'

default: usage

usage:
	@echo
	@echo 'Usage: make <action>'
	@echo
	@echo '    setup                install dependencies'
	@echo '    test                 run unit tests'

setup:
	@$(PIP) install -r requirements.txt

test:
	@$(PYTEST)
