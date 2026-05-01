# TaskFlow API — atalhos de desenvolvimento (requer GNU Make no PATH)
# Uso: make test | make run | make install | make migrate

PYTHON := .venv/Scripts/python.exe
PIP := $(PYTHON) -m pip

.PHONY: help install test test-verbose run migrate migrate-downgrade clean-pycache

help:
	@echo Available targets:
	@echo   make install          - instala dependencias (requirements.txt)
	@echo   make test             - roda pytest em modo quiet
	@echo   make test-verbose     - roda pytest com saida verbosa
	@echo   make run              - sobe uvicorn com reload
	@echo   make migrate          - alembic upgrade head
	@echo   make migrate-downgrade - alembic downgrade -1
	@echo   make clean-pycache    - remove __pycache__ e .pyc

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

test-verbose:
	$(PYTHON) -m pytest -v

run:
	$(PYTHON) -m uvicorn app.main:app --reload

migrate:
	$(PYTHON) -m alembic upgrade head

migrate-downgrade:
	$(PYTHON) -m alembic downgrade -1

clean-pycache:
	@powershell -NoProfile -Command "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Get-ChildItem -Recurse -Filter '*.pyc' | Remove-Item -Force -ErrorAction SilentlyContinue"
