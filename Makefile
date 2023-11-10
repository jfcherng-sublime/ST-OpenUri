.PHONY: all
all:

.PHONY: ci-check
ci-check:
	mypy -p plugin
	flake8 .
	black --check --preview --diff .
	isort --check --diff .

.PHONY: ci-fix
ci-fix:
	autoflake --in-place .
	black --preview .
	isort .
