POETRY:=venv/bin/poetry

venv: venv/bin/activate

venv/bin/activate: poetry.lock
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install poetry
	venv/bin/poetry install
	touch venv/bin/activate

isort: venv
	$(POETRY) run isort .

black: venv
	$(POETRY) run black .

build: venv
	$(POETRY) build

formatting: isort black

test: venv
	$(POETRY) run pytest -v tests
