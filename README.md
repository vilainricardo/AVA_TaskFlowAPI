# TaskFlow API

[![Python](https://img.shields.io/badge/python-3.13+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Sumário
- [Resumo / Summary](#resumo)
- [Objetivo / Purpose](#objetivo)
- [Funcionalidades / Features](#funcionalidades)
- [Stack Tecnológica / Tech Stack](#stack-tecnologica)
- [Requisitos / Requirements](#requisitos)
- [Configuração / Configuration](#configuracao)
- [Instalação / Installation](#instalacao)
- [Banco de dados / Database](#banco-de-dados)
- [Execução / Running](#execucao)
- [Testes / Tests](#testes)
- [Comandos make / Make commands](#comandos-make)
- [Endpoints](#endpoints)
- [Exemplos de uso / Usage examples](#exemplos-de-uso)
- [Estrutura do projeto / Project structure](#estrutura-do-projeto)
- [Observações importantes / Important notes](#observacoes-importantes)
- [Uso de IA no projeto / AI-assisted development](#uso-de-ia-no-projeto)

## Resumo
TaskFlow API é uma API REST para gerenciamento de tarefas, desenvolvida com FastAPI, SQLAlchemy, PostgreSQL e Alembic. O projeto foi pensado como uma base acadêmica clara, organizada e pronta para crescer.

## Summary
TaskFlow API is a REST API for task management, built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic. The project was designed as an organized, educational base that is easy to understand and ready for future growth.

## Objetivo
O objetivo do projeto é mostrar uma API simples, mas bem estruturada, para criar, consultar, atualizar e acompanhar tarefas. Além de atender ao contexto acadêmico, ele também funciona como exemplo de organização de backend em Python.

## Purpose
The goal of the project is to demonstrate a simple but well-structured API for creating, reading, updating, and tracking tasks. Besides being an academic project, it also serves as an example of backend organization in Python.

## Funcionalidades
- Criar tarefas
- Listar tarefas com filtros por status, prioridade e texto
- Listar tarefas com paginação (`limit` e `offset`)
- Consultar uma tarefa pelo ID
- Atualizar dados da tarefa
- Alterar o status da tarefa para concluída
- Reabrir uma tarefa concluída
- Excluir uma tarefa
- Manter histórico de auditoria das alterações
- Expor health check e documentação automática
- Retornar erros em formato padronizado (`error.code`, `error.message`, `error.details`, `error.trace_id`)

## Features
- Create tasks
- List tasks with filters by status, priority, and text search
- List tasks with pagination (`limit` and `offset`)
- Get a task by ID
- Update task data
- Move a task to the completed status
- Reopen a completed task
- Delete a task
- Keep an audit history of changes
- Expose a health check and automatic documentation
- Return errors using a standardized format (`error.code`, `error.message`, `error.details`, `error.trace_id`)

## Stack Tecnológica
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest

## Requisitos
- Python 3.13 ou compatível
- PostgreSQL em execução local ou acesso a uma string de conexão válida
- `pip` disponível

## Requirements
- Python 3.13 or compatible
- PostgreSQL running locally or a valid connection string
- `pip` available

## Configuração
Copie o arquivo `.env.example` para `.env` e ajuste os valores conforme o seu ambiente.

```env
APP_NAME=TaskFlow API
API_V1_PREFIX=/api/v1
ENVIRONMENT=local
SQLALCHEMY_ECHO=false

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=

# Optional. If set, it overrides the individual POSTGRES_* values above.
DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/taskflow
```

## Configuration
Copy `.env.example` to `.env` and adjust the values for your environment.

```env
APP_NAME=TaskFlow API
API_V1_PREFIX=/api/v1
ENVIRONMENT=local
SQLALCHEMY_ECHO=false

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=

# Optional. If set, it overrides the individual POSTGRES_* values above.
DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/taskflow
```

## Instalação
Crie e ative o ambiente virtual e, em seguida, instale as dependências.

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Se você usar outro shell, ative o ambiente virtual com o comando equivalente.

## Installation
Create and activate the virtual environment, then install the dependencies.

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If you use another shell, activate the virtual environment with the equivalent command for your system.

## Banco de dados
Antes de iniciar a aplicação, aplique as migrations:

```bash
alembic upgrade head
```

## Database
Before starting the application, run the migrations:

```bash
alembic upgrade head
```

## Execução
Inicie a aplicação com:

```bash
uvicorn app.main:app --reload
```

Depois disso, a API fica disponível em:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Running
Start the application with:

```bash
uvicorn app.main:app --reload
```

After that, the API is available at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Testes
Execute a suíte de testes com:

```bash
python -m pytest -q
```

A suíte usa um banco real e depende de PostgreSQL disponível e das migrations aplicadas.

## Tests
Run the test suite with:

```bash
python -m pytest -q
```

The suite uses a real database and depends on PostgreSQL being available and the migrations being applied.

## Comandos make
Na raiz do projeto existe um `Makefile`. Rode os comandos a partir da pasta deste repositório. Para ver os alvos com descrições curtas direto no terminal: `make help`.

Todos os alvos definidos hoje são:

| Comando | O que faz |
| --- | --- |
| `make help` | Mostra todos os alvos e uma linha de descrição cada |
| `make install` | Instala dependências (`requirements.txt`) com o pip do `.venv` |
| `make test` | Roda `pytest` em modo quiet (`-q`) |
| `make test-verbose` | Roda `pytest` com saída verbosa (`-v`) |
| `make run` | Sobe `uvicorn` em modo reload (`app.main:app`) |
| `make migrate` | Aplica migrações: `alembic upgrade head` |
| `make migrate-downgrade` | Volta uma revisão: `alembic downgrade -1` |
| `make clean-pycache` | Remove pastas `__pycache__` e arquivos `.pyc` (usa PowerShell no Windows) |

Todos usam `.venv/Scripts/python.exe`; crie e preencha o `.venv` antes conforme [Instalação](#instalacao).

**GNU Make no Windows**: instale uma vez com o gerenciador de pacotes (`winget`):

```powershell
winget install -e --id ezwinports.make --accept-package-agreements --accept-source-agreements
```

Depois da instalação, **feche e reabra o terminal** (ou reinicie o Cursor) para o `PATH` ser atualizado. Na mesma sessão do PowerShell, você pode atualizar manualmente:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") + ";" + $env:Path
make --version
```

## Make commands
There is a `Makefile` at the repository root. Run commands from this project folder. For short descriptions printed in the terminal, use `make help`.

All targets currently defined:

| Command | Description |
| --- | --- |
| `make help` | Prints every target and a one-line description |
| `make install` | Installs dependencies (`requirements.txt`) via the `.venv` pip |
| `make test` | Runs `pytest` in quiet mode (`-q`) |
| `make test-verbose` | Runs `pytest` with verbose output (`-v`) |
| `make run` | Starts `uvicorn` with reload (`app.main:app`) |
| `make migrate` | Applies migrations: `alembic upgrade head` |
| `make migrate-downgrade` | Rolls back one revision: `alembic downgrade -1` |
| `make clean-pycache` | Removes `__pycache__` directories and `.pyc` files (uses PowerShell on Windows) |

All of them use `.venv/Scripts/python.exe`; create and populate `.venv` first as described in [Installation](#installation).

**GNU Make on Windows**: install once with Windows Package Manager (`winget`):

```powershell
winget install -e --id ezwinports.make --accept-package-agreements --accept-source-agreements
```

After installation, **close and reopen your terminal** (or restart Cursor) so the updated `PATH` is picked up. Within the same PowerShell session you can refresh manually:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") + ";" + $env:Path
make --version
```

## Endpoints
Base path da API: `/api/v1`

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/tasks` | Cria uma tarefa |
| `GET` | `/tasks` | Lista tarefas com filtros opcionais e paginação (`limit`, `offset`) |
| `GET` | `/tasks/{task_id}` | Consulta uma tarefa pelo ID |
| `PUT` | `/tasks/{task_id}` | Atualiza uma tarefa |
| `PATCH` | `/tasks/{task_id}/complete` | Altera o status da tarefa para concluída |
| `PATCH` | `/tasks/{task_id}/reopen` | Reabre uma tarefa concluída |
| `DELETE` | `/tasks/{task_id}` | Exclui uma tarefa |
| `GET` | `/health` | Verifica se a aplicação e o banco estão acessíveis |

## Endpoints
API base path: `/api/v1`

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks with optional filters and pagination (`limit`, `offset`) |
| `GET` | `/tasks/{task_id}` | Get a task by ID |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `PATCH` | `/tasks/{task_id}/complete` | Mark a task as completed |
| `PATCH` | `/tasks/{task_id}/reopen` | Reopen a completed task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |
| `GET` | `/health` | Check whether the application and database are reachable |

## Exemplos de uso
Aqui estão alguns exemplos rápidos para consultas comuns na API.

## Usage examples
Here are some quick examples for common API calls.

### Criar uma tarefa / Create a task
Para criar uma task sem usar a interface do Swagger, você pode enviar uma requisição `POST` assim:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" -H "Content-Type: application/json" -d "{\"title\":\"Estudar testes\",\"description\":\"Revisar a cobertura\",\"status\":\"queued\",\"priority\":\"high\"}"
```

Resposta esperada:

```json
{
  "id": "uuid-gerado-pela-api",
  "title": "Estudar testes",
  "description": "Revisar a cobertura",
  "status": "queued",
  "priority": "high",
  "due_date": null,
  "created_at": "2026-05-01T12:00:00Z",
  "updated_at": "2026-05-01T12:00:00Z"
}
```

## Request example
To create a task without using the Swagger UI, you can send a `POST` request like this:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" -H "Content-Type: application/json" -d "{\"title\":\"Study tests\",\"description\":\"Review coverage\",\"status\":\"queued\",\"priority\":\"high\"}"
```

Expected response:

```json
{
  "id": "uuid-generated-by-the-api",
  "title": "Study tests",
  "description": "Review coverage",
  "status": "queued",
  "priority": "high",
  "due_date": null,
  "created_at": "2026-05-01T12:00:00Z",
  "updated_at": "2026-05-01T12:00:00Z"
}
```

### Listar tarefas / List tasks
Para listar tarefas com filtro e paginação, você pode usar uma requisição `GET`:

```bash
curl "http://127.0.0.1:8000/api/v1/tasks?status=queued&priority=high&text=study&limit=20&offset=0"
```

Response example:

```json
{
  "items": [
    {
      "id": "uuid-generated-by-the-api",
      "title": "Study tests",
      "description": "Review coverage",
      "status": "queued",
      "priority": "high",
      "due_date": null,
      "created_at": "2026-05-01T12:00:00Z",
      "updated_at": "2026-05-01T12:00:00Z"
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 1,
    "has_next": false
  }
}
```

### Erro padronizado / Standard error
Quando ocorrer erro de validação, domínio ou falha interna, a API responde no formato padrão:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request payload validation failed.",
    "details": [
      {
        "field": "priority",
        "message": "Input should be 'low', 'medium', 'high' or 'urgent'"
      }
    ],
    "trace_id": "uuid-generated-by-the-api"
  }
}
```

### Atualizar uma tarefa / Update a task
Para atualizar apenas alguns campos, envie um `PUT` com o payload desejado:

```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/tasks/<task_id>" -H "Content-Type: application/json" -d "{\"title\":\"Task atualizada\",\"status\":\"in_progress\",\"priority\":\"urgent\"}"
```

### Excluir uma tarefa / Delete a task
Para remover uma tarefa, use `DELETE`:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/tasks/<task_id>"
```

## Estrutura do projeto
```text
app/
  core/         configuração e bootstrap do banco
  dtos/         contratos de request e response por domínio
  models/       models ORM do SQLAlchemy
  repositories/ acesso ao banco
  routers/      rotas do FastAPI
  services/     regras de negócio
migrations/     migrations do Alembic
tests/          testes de service e API
docs/           documentos de requisitos e arquitetura
```

## Project structure
```text
app/
  core/         configuration and database bootstrap
  dtos/         request and response contracts grouped by domain
  models/       SQLAlchemy ORM models
  repositories/ database access layer
  routers/      FastAPI routes
  services/     business rules
migrations/     Alembic migrations
tests/          service and API tests
docs/           requirements and architecture documents
```

## Observações importantes
- O histórico de auditoria da task é preservado mesmo depois da exclusão da task.
- A auditoria é interna ao domínio e, por enquanto, não tem endpoints próprios.
- Os contratos da API foram separados em requests e responses por domínio para facilitar a expansão futura.
- O projeto foi organizado para ficar claro para quem está aprendendo e para quem vai manter o código depois.

## Important notes
- Task audit history is preserved even after deleting the task.
- Audit records are internal to the domain and do not have dedicated endpoints for now.
- API contracts are split into requests and responses by domain to make future expansion easier.
- The project was organized to be clear for learners and maintainable for future contributors.

## Uso de IA no projeto
Este repositório foi desenvolvido com apoio de ferramentas de IA, em etapas distintas:

1. **Documentação inicial (Vision e preparação de SRS)**  
   Utilizou-se um agente previamente configurado para produzir documentos tipo *Vision*, a partir do que seria o escopo do projeto. Isso gerou:
   - [`docs/vision_document_task_flow_api.md`](docs/vision_document_task_flow_api.md) — visão geral do produto/API  
   - [`docs/srs_preparation_document_task_flow_api.md`](docs/srs_preparation_document_task_flow_api.md) — notas úteis para a elaboração do SRS  

2. **SRS e material de suporte ao SAD**  
   Em seguida, outro agente recebeu o vision document e material de suporte com dados extras e produziu:
   - [`docs/task_flow_api_srs_final.md`](docs/task_flow_api_srs_final.md)  
   - [`docs/task_flow_api_sad_support_document.md`](docs/task_flow_api_sad_support_document.md) — apoio à redação do SAD  

3. **SAD e diagramas**  
   Por fim, usou-se um agente focado na criação de documentos SAD a partir do SRS e de um documento adicional com informações pertinentes à arquitetura. Essa etapa gerou:
   - [`docs/sad_task_flow_api_enterprise.md`](docs/sad_task_flow_api_enterprise.md)  
   - Os artefatos em [`diagrams/`](diagrams/)  

   Todo esse fluxo de **documentação** foi realizado **no ChatGPT pelo navegador**.

4. **Implementação em código**  
   Com os documentos acima como referência, a **implementação do programa** (incluindo refatorações) foi feita com **Codex em linha de comando**, priorizando **coerência entre documentação e código**.

5. **Revisão de testes**  
   Na etapa de **revisão e fortalecimento dos testes** utilizou-se o **Cursor**.

## AI-assisted development
This repository was built with AI assistance across several phases:

1. **Initial documentation (Vision and SRS preparation)**  
   A dedicated agent produced *Vision*-style artifacts from an initial project outline, generating:
   - [`docs/vision_document_task_flow_api.md`](docs/vision_document_task_flow_api.md) — high-level vision  
   - [`docs/srs_preparation_document_task_flow_api.md`](docs/srs_preparation_document_task_flow_api.md) — notes to support SRS drafting  

2. **SRS and SAD-support material**  
   Another agent took the vision document plus supporting inputs and produced:
   - [`docs/task_flow_api_srs_final.md`](docs/task_flow_api_srs_final.md)  
   - [`docs/task_flow_api_sad_support_document.md`](docs/task_flow_api_sad_support_document.md) — support for the SAD document  

3. **SAD and diagrams**  
   A SAD-focused agent then produced enterprise-style architecture documentation from the SRS and extra architecture-oriented material:
   - [`docs/sad_task_flow_api_enterprise.md`](docs/sad_task_flow_api_enterprise.md)  
   - The diagram assets under [`diagrams/`](diagrams/)  

   This entire **documentation** workflow ran **in ChatGPT via the browser**.

4. **Code implementation**  
   With those documents as inputs, **application code** (including refactorings) was authored using **Codex from the command line**, aiming to keep **requirements/architecture docs and implementation aligned**.

5. **Test review**  
   **Cursor** was used when reviewing and improving the test suite.
