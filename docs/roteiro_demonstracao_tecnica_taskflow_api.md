# Roteiro de demonstração técnica — TaskFlow API

Este documento descreve **como preparar**, **demonstrar** e **submeter** o projeto de forma didática e repetível — incluindo **empacotamento**, **cenário da demo ao vivo**, e **entregáveis de submissão**. Alinha-se ao código em `AVA_TaskFlowAPI/` (FastAPI + SQLAlchemy + PostgreSQL + Alembic).

---

## 1. Objetivo

- Dar visibilidade clara ao **valor do sistema** (API de tarefas com filtros, paginação, auditoria descrita nos documentos da pasta `docs/` e nos endpoints).
- Garantir que o avaliador (ou público técnico) consiga **reproduzir** o cenário ou validar pela documentação automatizada (**OpenAPI** em `/docs`).

---

## 2. Audiência e formato sugerido

| Aspecto | Sugestão |
| --- | --- |
| Audiência típica | Professor, banca, cliente técnico, colegas de squad |
| Duração total | **8 a 15 minutos** na demo gravada ao vivo ou **slides + hands-on** |
| Ferramentas | Navegador (Swagger/ReDoc), terminal (opcional `curl`/HTTPie), cliente REST (Thunder Client, Postman) |

---

## 3. Empacotamento (o que deixar “pronto para rodar ou mostrar”)

### 3.1 Conteúdo mínimo do pacote-fonte

Garantir que existam na raiz do projeto da API (`AVA_TaskFlowAPI/`):

- `README.md` — configurar `.env`, venv, migrations, execução e testes.
- `requirements.txt` — dependências para `pip install -r`.
- `.env.example` — variáveis **sem secrets** para o avaliador copiar (`cp` / cópia manual).
- `Makefile` *(opcional para quem usar GNU Make)* — atalhos (`make test`, `make migrate`, etc.).
- `app/` — código da aplicação.
- `migrations/` — histórico Alembic aplicável com `alembic upgrade head`.
- `tests/` — suíte Pytest contra banco real.
- `docs/` — documentação de produto/arquitetura (Vision, SRS, SAD, backlog, este roteiro).
- `diagrams/` *(se usar na apresentação)* — artefatos de arquitetura.

### 3.2 O que não empacotar

- `.env` com **senhas reais** ou tokens (usar apenas variáveis de exemplo).
- Pasta `.venv`** completa**, se submissão for por arquivo compactado grande — prefira README + `.env.example` + `requirements.txt` e instruir criação do venv localmente.

### 3.3 Congelamento opcional das dependências (antes de submeter)

Para reprodutibilidade máxima em ambientes academia/banca:

```bash
.\.venv\Scripts\pip.exe freeze > requirements-lock.txt
```

Anexe `requirements-lock.txt` **somente se** sua instituição exigir bit-a-bit igual; caso contrário, `requirements.txt` já costuma bastar para o MVP.

### 3.4 Checklist de empacotamento (antes da demo/submissão)

- [ ] `alembic upgrade head` aplicado sem erro contra um PostgreSQL em branco configurado pelo `.env`.
- [ ] `python -m pytest -q` (ou `make test`) — **passa** com o mesmo banco/migrations esperados pelo README.
- [ ] Servidor sobe (`uvicorn` ou `make run`) sem stack trace ao chamar `/health`.
- [ ] OpenAPI atualizado em `/docs` com os endpoints e modelos esperados (`GET /tasks` com objeto paginado, erros padronizados quando aplicável).
- [ ] Documentos obrigatórios da instituição estão nomeados conforme solicitado na pasta `docs/`.

---

## 4. Preparação do ambiente de demonstração (mesmo fluxo antes de gravar)

1. PostgreSQL disponível (`localhost` ou máquina de laboratório).
2. Copiar `.env.example` → `.env` e ajustar `POSTGRES_*` ou `DATABASE_URL`.
3. Criar/ativar venv e dependências conforme README.
4. `alembic upgrade head` (ou `make migrate`).
5. `uvicorn app.main:app --reload` ou `make run`.
6. Abrir `http://127.0.0.1:8000/docs` e `GET /health` para garantir estado “verde”.

---

## 5. Roteiro da demonstração técnica (passo a passo)

Cronograma sugerido (**~12 min**). Adapte se banca curtir bem ou mal tempo.

### 5.1 Abertura (1–2 min)

- **Pitch**: uma frase sobre o problema (gestão de tarefas) e uma sobre a solução (API REST com persistência + auditoria no domínio, conforme documentação).
- **Arquitetura em uma lâmina**: apontar `routers/` → `services/` → `repositories/` → `models/` (diagrama rápido de `diagrams/` se já existir).

### 5.2 Contrato HTTP e documentação ao vivo (2 min)

- Abrir Swagger (`/docs`).
- Destacar: `POST`, `GET /tasks`, `GET /tasks/{id}`, `PUT`, `PATCH …/complete`, `PATCH …/reopen`, `DELETE`.

### 5.3 Happy path com dados (5–6 min)

Execute na ordem (via Swagger ou copiar coleção Postman):

1. **`POST /api/v1/tasks`** — criar tarefa com `title`, `priority`, opcionalmente `due_date`; confirmar **`201`** e corpo com `id`, timestamps.
2. **`GET /api/v1/tasks`** — usar filtros `status`, `priority`, `text` e **`limit`/`offset`**; mostrar objeto `items` + `pagination` (`total`, `has_next`).
3. **`GET /api/v1/tasks/{task_id}`** — ler a tarefa recém criada (**`200`**).
4. **`PUT /api/v1/tasks/{task_id}`** — atualizar título/descrição/status/prioridade; mostrar **`200`** e `updated_at` alterado conceptualmente (ou campo visível na resposta).
5. **`PATCH …/complete`** — status `completed`; em seguida **`PATCH …/reopen`** — voltar fluxo esperado (**`queued`** ou conforme regra atual do serviço).
6. **`DELETE /api/v1/tasks/{task_id}`** — **`204`** e depois **`GET`** na mesma `id` retornando **`404`** no formato padronizado de erro (se projeto estiver assim configurado).

### 5.4 Casos limite rápidos (2 min)

Mostrar pelo menos dois:

- **Payload inválido** em `POST /tasks` (ex.: `priority` ilegal) → **`422`** + corpo `error` com código/mensagem.
- **UUID ou ID inexistente** em operações que exigem tarefa existente → **`404`** adequado ao contrato público atual.

### 5.5 Qualidade automatizada e encerramento (1–2 min)

- Mostrar comando `pytest` ou `make test` no terminal (**verde**) como evidência objetiva de regressão mínima.
- Fechar relacionando decisões aos documentos SRS/SAD se a banca exigir traçabilidade.

---

## 6. Demonstração gravada ou remota — dicas rápidas

- **Áudio/clareza**: fale só o necessário durante os cliques; evite ler JSON inteiro campo a campo salvo pedagogia específica.
- **Credenciais**: se gravar vídeo com tela inteira do `.env`, **use senha fake** apenas para aquele momento.
- **Latência**: se rede do laboratório for instável, tenha segundo plano (**Postman coleção offline** já importada ou script `curl` pronto).

---

## 7. Submissão (pacote de entrega)

### 7.1 Entregáveis típicos (ajuste aos requisitos da disciplina/projeto corporativo)

| Item | Observação |
| --- | --- |
| Código-fonte | Repositório Git (preferencial) ou **ZIP único sem `node_modules`/`__pycache__/` `.venv`** se possível |
| README | Como instalar, migrar e rodar (já existente na raiz) |
| Esta documentação de roteiro | Arquivo atual em `docs/` |
| Documentação SRS/SAD/Vision | Conforme `docs/` do repositório |
| Evidências de execução | *(opcional obrigatório)* PDF com prints **`/health`**, **`POST` bem-sucedido**, lista paginada, erro típico; ou link de vídeo |
| Lista de comandos reproducíveis | Ex.: comandos README + `pytest` ao final |

### 7.2 Checklist antes de enviar ao avaliador

- [ ] Link do repo ou arquivo ZIP abre sem senha estranha; **estrutura** idêntica à esperada.
- [ ] Instrução explícita: versão Python (≥ 3.13 conforme projeto) + PostgreSQL.
- [ ] Migrations funcionam contra banco novo (cenário típico de correção automatizada/manual).
- [ ] Um **script bloco único** (PowerShell/bash) opcional só com comandos já testados você mesmo no dia (**reduz retrabalho** do professor).

---

## 8. Riscos frequentes na correção externa — mitigações

| Risco | Mitigação |
| --- | --- |
| Postgres não configurado ou porta errada | `.env.example` comentando cada variável; README com exemplo de URL |
| Migrations ignoradas alembic não roda ao subir primeira vez | Deixar `make migrate` e README em destaque no roteiro de submissão |
| Divergência OpenAPI × código antigo na gravação | Registrar demo **imediatamente** após último merge estável |

---

## 9. Extensões opcionais (se quiser pontuação ou portfólio extra)

Não fazem parte do núcleo mínimo; podem aparecer como “trabalhos futuros” na apresentação:

- Imagem Docker com PostgreSQL embutido (compose) para avaliador zerar infra em um comando.
- CI (GitHub Actions) rodando `pytest` contra serviço de banco de testes.
- OpenAPI exportado como `openapi.json` versionado apenas se sua política aceitar esse artefato estático.

---

**Fim do roteiro.** Ajuste seções obrigatórias à norma institucional (capa, APA, relatório técnico, etc.) antes de imprimir/anexar.
