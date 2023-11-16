.PHONY: all
all:

.PHONY: install
install:
	python -m pip install -U pip -r requirements.txt

.PHONY: ci-check
ci-check:
	mypy -p plugin
	ruff check --diff --preview .
	black --diff --preview --check .

.PHONY: ci-fix
ci-fix:
	ruff check --preview --fix .
	# ruff format --preview .
	black --preview .
