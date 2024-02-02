.PHONY: all
all:

.PHONY: install
install:
	python -m pip install -U pip -r requirements.txt

.PHONY: ci-check
ci-check:
	mypy -p plugin
	ruff check --diff .
	ruff format --diff .

.PHONY: ci-fix
ci-fix:
	ruff check --fix .
	ruff format .
