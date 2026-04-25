# TaskFlow API — Software Requirements Specification (SRS)

## Quality Gate
Score Final: 9.3/10

## 1. Visão Geral
Micro-API REST para gerenciamento de tarefas usando FastAPI e PostgreSQL.

## 2. Escopo MVP
Criar, listar, consultar, atualizar, concluir, reabrir e excluir tarefas com documentação automática.

## 3. Assumptions
- Projeto acadêmico individual
- Deploy local
- Sem autenticação no MVP
- PostgreSQL local

## 4. Glossário Técnico
- Task: tarefa cadastrada
- CRUD: criar, ler, atualizar, excluir
- Endpoint: rota HTTP
- MVP: versão mínima viável

## 5. Modelo de Dados
- id
- title
- description
- completed
- priority
- due_date
- created_at
- updated_at

## 6. Requisitos Funcionais

### FR-001
- ID: FR-001
- Nome: Criar tarefa
- Descrição: Permitir cadastro de tarefa.
- Regras de Negócio: title obrigatório.
- Prioridade: Must
- Dependências: Banco disponível
- Teste:
  - POST /tasks com title válido retorna 201.
  - POST sem title retorna 422.

### FR-002
- ID: FR-002
- Nome: Listar tarefas
- Descrição: Listar tarefas cadastradas.
- Regras de Negócio: filtros por status, prioridade e texto.
- Prioridade: Must
- Dependências: FR-001
- Teste:
  - GET /tasks retorna 200.
  - GET filtrado retorna itens coerentes.

### FR-003
- ID: FR-003
- Nome: Consultar tarefa por ID
- Descrição: Retornar tarefa específica.
- Regras de Negócio: inexistente retorna 404.
- Prioridade: Must
- Dependências: FR-001
- Teste:
  - GET /tasks/{id} válido retorna 200.
  - GET inválido retorna 404.

### FR-004
- ID: FR-004
- Nome: Atualizar tarefa
- Descrição: Alterar dados permitidos.
- Regras de Negócio: updated_at atualizado.
- Prioridade: Must
- Dependências: FR-001
- Teste:
  - PUT /tasks/{id} retorna 200.

### FR-005
- ID: FR-005
- Nome: Concluir tarefa
- Descrição: Marcar como concluída.
- Regras de Negócio: completed=true.
- Prioridade: Must
- Dependências: FR-001
- Teste:
  - PATCH /tasks/{id}/complete retorna 200.

### FR-006
- ID: FR-006
- Nome: Reabrir tarefa
- Descrição: Reabrir tarefa concluída.
- Regras de Negócio: completed=false.
- Prioridade: Should
- Dependências: FR-005
- Teste:
  - PATCH /tasks/{id}/reopen retorna 200.

### FR-007
- ID: FR-007
- Nome: Excluir tarefa
- Descrição: Remover tarefa.
- Regras de Negócio: exclusão física no MVP.
- Prioridade: Must
- Dependências: FR-001
- Teste:
  - DELETE /tasks/{id} retorna 204.

## 7. Requisitos Não Funcionais
- NFR-001 p95 < 300ms local.
- NFR-002 Cobertura de testes >= 80%.
- NFR-003 Código modular.
- NFR-004 Logs padronizados.
- NFR-005 Swagger/OpenAPI disponível.

## 8. Endpoints
- POST /tasks
- GET /tasks
- GET /tasks/{id}
- PUT /tasks/{id}
- PATCH /tasks/{id}/complete
- PATCH /tasks/{id}/reopen
- DELETE /tasks/{id}

## 9. Matriz de Rastreabilidade
- CRUD: FR-001,002,003,004,007
- Workflow: FR-005,006
- Qualidade: NFR-001..005

