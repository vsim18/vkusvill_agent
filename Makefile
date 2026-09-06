.PHONY: install test lint format format-check run

install:
	python3.12 -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

run:
	python3.12 -m app

