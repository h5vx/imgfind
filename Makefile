isort:
	isort .

black:
	black .

formatting: isort black

test:
	pytest -v tests
