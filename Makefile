.PHONY: all
all: fix

.PHONY: check
check:
	mypy -p plugin
	flake8 .
	black --preview --check --diff .
	isort --check --diff .

.PHONY: fix
fix:
	autoflake --in-place .
	black . --preview
	isort .
