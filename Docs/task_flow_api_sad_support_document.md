# TaskFlow API — SAD Support Document

## 1. Objetivo
Suportar futura elaboração do Software Architecture Document (SAD).

## 2. Considerações Arquiteturais
- FastAPI como camada HTTP.
- SQLAlchemy ORM.
- PostgreSQL persistência principal.
- Pydantic validação.
- Pytest para testes.

## 3. Estrutura Recomendada
- app/main.py
- app/routers/
- app/services/
- app/repositories/
- app/models/
- app/dtos/
- tests/

## 4. Decisões Técnicas em Aberto
- UUID ou integer para chave primária.
- Soft delete vs hard delete futuro.
- Paginação offset/limit ou cursor.
- Prefixo /api/v1.

## 5. Riscos Técnicos
- Crescimento sem versionamento.
- Baixa cobertura de testes.
- Acoplamento entre camadas.
- Falta de padronização de erros.

## 6. Mitigações
- Introduzir versionamento desde início.
- CI com lint + tests.
- Service layer explícita.
- Error schema padronizado.

## 7. Direção Recomendada
- UTC para timestamps.
- Alembic para migrations.
- .env para configurações.
- Fixtures de teste isoladas.

## 8. Roadmap Técnico
- MVP: CRUD + docs + testes.
- v1.1: autenticação.
- v1.2: categorias/tags.
- v2: multiusuário.

## 9. Dependências Prováveis
- fastapi
- uvicorn
- sqlalchemy
- psycopg2 ou asyncpg
- pydantic
- pytest
- alembic

