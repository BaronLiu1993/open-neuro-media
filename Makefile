.PHONY: setup dev build test clean

setup:
	docker compose up --build -d
	@echo ""
	@echo "Done. App running at http://localhost:8000, MongoDB at localhost:27017"

dev:
	.venv/bin/uvicorn main:app --reload

test:
	.venv/bin/pytest tests/ -v

build:
	docker build -t neuro .

clean:
	rm -rf .venv __pycache__ .pytest_cache cache
