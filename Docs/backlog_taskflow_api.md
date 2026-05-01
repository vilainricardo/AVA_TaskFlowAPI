# TaskFlow API - Backlog Detalhado

Este backlog foi revisado com base no código, nos testes, nas migrations, na documentação e nos diagramas já presentes no projeto. Estão marcados apenas os itens que existem com segurança no estado atual. O que não estiver marcado deve ser tratado como pendente ou ainda não confirmado.

## Resumo visual

| Fase | Status | Leitura rápida |
| --- | --- | --- |
| Fase 1 - Planejamento e definição do produto | Parcial | Base conceitual definida, mas ainda há pontos abertos de erro, aceitação e paginação. |
| Fase 2 - Preparação do ambiente | Concluída | Ferramentas, configuração e banco de desenvolvimento estão definidos. |
| Fase 3 - Estrutura do projeto | Concluída | Pastas, camadas e convenções já estão estabelecidas. |
| Fase 4 - Modelagem de dados | Concluída | Task e TaskAudit já estão modeladas e persistidas. |
| Fase 5 - DTOs e contratos da API | Concluída | Requests e responses estão organizados por domínio. |
| Fase 6 - Repositório | Concluída | CRUD, filtros e ordenação já existem. |
| Fase 7 - Service layer | Concluída | Regras de negócio e auditoria estão implementadas. |
| Fase 8 - Camada HTTP | Concluída | Endpoints da API principal já estão expostos. |
| Fase 9 - Tratamento de erros | Parcial | Erros de domínio e validação estão cobertos, mas falhas inesperadas ainda não estão formalizadas. |
| Fase 10 - Testes | Concluída | Service, API e regressão têm cobertura relevante. |
| Fase 11 - Documentação | Concluída | README, docs e diagramas já foram atualizados. |
| Fase 12 - Qualidade e manutenção | Parcial | Organização e evolução estão encaminhadas, mas a manutenção contínua segue em aberto. |

**Legenda**
- Concluída: praticamente tudo da fase existe no estado atual.
- Parcial: a maior parte existe, mas há itens ainda abertos ou não confirmados.
- Pendente: a fase não está concluída.

## Como usar

- Marque cada item concluído com `x`.
- Use este arquivo como uma visão geral do progresso real do projeto.
- Se surgir dúvida sobre um item, mantenha-o desmarcado.
- Atualize este backlog sempre que houver mudança relevante no código ou na documentação.

## Fase 1: Planejamento e definição do produto

**Status geral:** Parcial

### 1.1 Objetivo e escopo
- [x] Definir o objetivo principal da API
- [x] Definir o público-alvo do sistema
- [x] Definir o problema que a API resolve
- [x] Definir o que entra no MVP
- [x] Definir o que fica fora do MVP
- [x] Definir as principais entidades do domínio
- [x] Definir o nome do projeto e o nome da API

### 1.2 Regras de negócio
- [x] Definir o que é uma task no contexto do sistema
- [x] Definir quais campos a task deve possuir
- [x] Definir quais campos são obrigatórios
- [x] Definir quais campos são opcionais
- [x] Definir quais estados uma task pode assumir
- [x] Definir quando uma task pode ser concluída
- [x] Definir quando uma task pode ser reaberta
- [x] Definir a regra de exclusão de task
- [x] Definir a regra de auditoria
- [x] Definir quais mudanças devem ser auditadas

### 1.3 Requisitos funcionais
- [x] Listar todos os endpoints do MVP
- [x] Definir o comportamento esperado de cada endpoint
- [x] Definir códigos HTTP esperados por cenário
- [ ] Definir mensagens de erro padrão
- [ ] Definir critérios de aceitação por endpoint
- [x] Definir filtros disponíveis na listagem
- [x] Definir regras de ordenação
- [ ] Definir necessidade de paginação

### 1.4 Requisitos não funcionais
- [x] Definir meta de desempenho
- [x] Definir meta mínima de cobertura de testes
- [x] Definir padrão de logs
- [x] Definir padrão de documentação
- [x] Definir padrão de organização do código
- [x] Definir estratégia de versionamento da API

## Fase 2: Preparação do ambiente

**Status geral:** Concluída

### 2.1 Ferramentas
- [x] Definir versão do Python
- [x] Definir dependências principais do projeto
- [x] Criar arquivo de dependências
- [x] Definir ferramenta de migração
- [x] Definir ferramenta de testes
- [x] Definir ferramenta de documentação local

### 2.2 Configuração inicial
- [x] Criar arquivo de configuração de ambiente
- [x] Criar exemplo de variáveis de ambiente
- [x] Definir nome da aplicação
- [x] Definir prefixo de API
- [x] Definir configuração de banco de dados
- [x] Definir configuração de ambiente local
- [x] Definir configuração de echo de SQL

### 2.3 Banco de dados local
- [x] Definir banco de dados principal
- [x] Definir credenciais de desenvolvimento
- [x] Definir estratégia de conexão
- [x] Validar conexão com o banco
- [x] Definir política de timestamps em UTC

## Fase 3: Estrutura do projeto

**Status geral:** Concluída

### 3.1 Organização de pastas
- [x] Criar pasta `app/core`
- [x] Criar pasta `app/models`
- [x] Criar pasta `app/repositories`
- [x] Criar pasta `app/services`
- [x] Criar pasta `app/routers`
- [x] Criar pasta `app/dtos`
- [x] Criar pasta `tests`
- [x] Criar pasta `docs`
- [x] Criar pasta `diagrams`

### 3.2 Arquitetura em camadas
- [x] Definir responsabilidades da camada HTTP
- [x] Definir responsabilidades da camada de serviço
- [x] Definir responsabilidades da camada de repositório
- [x] Definir responsabilidades da camada de modelo
- [x] Definir responsabilidades da camada de DTO
- [x] Definir como as camadas vão se comunicar

### 3.3 Convenções de código
- [x] Definir padrão de nomes para arquivos
- [x] Definir padrão de nomes para classes
- [x] Definir padrão de nomes para funções
- [x] Definir padrão de nomes para variáveis
- [x] Definir padrão de imports
- [x] Definir padrão de comentários e docstrings

## Fase 4: Modelagem de dados

**Status geral:** Concluída

### 4.1 Entidade principal: Task
- [x] Definir a tabela `tasks`
- [x] Definir a chave primária
- [x] Definir o campo `title`
- [x] Definir o campo `description`
- [x] Definir o campo `completed`
- [x] Definir o campo `priority`
- [x] Definir o campo `due_date`
- [x] Definir o campo `created_at`
- [x] Definir o campo `updated_at`

### 4.2 Regras do model
- [x] Definir valores padrão
- [x] Definir campos obrigatórios
- [x] Definir campos opcionais
- [x] Definir tipo de dados de cada campo
- [x] Definir limites de tamanho e validade
- [x] Definir comportamento de atualização automática de timestamps

### 4.3 Índices
- [x] Criar índice para `completed`
- [x] Criar índice para `priority`
- [x] Criar índice para `due_date`
- [x] Criar índice para `created_at`
- [x] Validar se os índices atendem os filtros previstos

### 4.4 Entidade de auditoria
- [x] Definir a tabela `task_audit`
- [x] Definir a chave primária
- [x] Definir o campo `task_id`
- [x] Definir o campo `action`
- [x] Definir o campo `before_state`
- [x] Definir o campo `after_state`
- [x] Definir o campo `created_at`
- [x] Definir a estratégia de preservação do histórico

## Fase 5: DTOs e contratos da API

**Status geral:** Concluída

### 5.1 Requests de task
- [x] Criar contrato de criação de task
- [x] Criar contrato de atualização de task
- [x] Criar contrato de filtro de listagem
- [x] Criar contrato de concluir task
- [x] Criar contrato de reabrir task

### 5.2 Responses de task
- [x] Criar contrato de resposta da task
- [x] Garantir que a resposta inclua os campos corretos
- [x] Garantir que a resposta seja serializável em JSON
- [x] Garantir conversão correta de timestamps

### 5.3 Auditoria
- [x] Criar contrato base de auditoria
- [x] Criar contrato de criação de auditoria
- [x] Criar contrato de resposta de auditoria
- [x] Definir se a auditoria será exposta publicamente ou apenas internamente

### 5.4 Validações
- [x] Validar comprimento mínimo e máximo de `title`
- [x] Validar prioridade mínima
- [x] Validar campos obrigatórios
- [x] Validar campos opcionais
- [x] Validar filtros vazios e parciais

## Fase 6: Repositório

**Status geral:** Concluída

### 6.1 CRUD básico
- [x] Criar método para adicionar task
- [x] Criar método para buscar task por ID
- [x] Criar método para listar tasks
- [x] Criar método para deletar task
- [x] Garantir flush nas operações necessárias

### 6.2 Busca e filtros
- [x] Implementar filtro por conclusão
- [x] Implementar filtro por prioridade
- [x] Implementar busca textual
- [x] Implementar ordenação da listagem
- [x] Garantir comportamento previsível quando não houver resultados

### 6.3 Auditoria de persistência
- [x] Definir como registrar auditoria ao criar task
- [x] Definir como registrar auditoria ao atualizar task
- [x] Definir como registrar auditoria ao concluir task
- [x] Definir como registrar auditoria ao reabrir task
- [x] Definir como registrar auditoria ao excluir task

## Fase 7: Service layer

**Status geral:** Concluída

### 7.1 Criação
- [x] Implementar criação de task
- [x] Garantir aplicação dos valores recebidos
- [x] Garantir persistência no banco
- [x] Garantir criação da auditoria de criação

### 7.2 Listagem
- [x] Implementar listagem de tasks
- [x] Aplicar filtros recebidos
- [x] Garantir retorno consistente

### 7.3 Consulta individual
- [x] Implementar busca de task por ID
- [x] Tratar task inexistente
- [x] Definir erro de domínio para não encontrado

### 7.4 Atualização
- [x] Implementar atualização de task
- [x] Permitir atualização parcial dos campos válidos
- [x] Atualizar `updated_at`
- [x] Registrar auditoria de atualização

### 7.5 Conclusão e reabertura
- [x] Implementar marcação de task como concluída
- [x] Implementar reabertura de task
- [x] Atualizar `updated_at` nessas transições
- [x] Registrar auditoria para cada transição

### 7.6 Exclusão
- [x] Implementar exclusão de task
- [x] Garantir que a task seja removida do catálogo principal
- [x] Registrar auditoria de exclusão
- [x] Garantir preservação do histórico de auditoria

## Fase 8: Camada HTTP

**Status geral:** Concluída

### 8.1 Router de task
- [x] Criar endpoint `POST /tasks`
- [x] Criar endpoint `GET /tasks`
- [x] Criar endpoint `GET /tasks/{task_id}`
- [x] Criar endpoint `PUT /tasks/{task_id}`
- [x] Criar endpoint `PATCH /tasks/{task_id}/complete`
- [x] Criar endpoint `PATCH /tasks/{task_id}/reopen`
- [x] Criar endpoint `DELETE /tasks/{task_id}`

### 8.2 Respostas HTTP
- [x] Definir `201 Created` para criação
- [x] Definir `200 OK` para leitura e atualização
- [x] Definir `204 No Content` para exclusão
- [x] Definir `404 Not Found` para task inexistente
- [x] Definir `422 Unprocessable Entity` para payload inválido

### 8.3 OpenAPI
- [x] Documentar summary de cada endpoint
- [x] Documentar description de cada endpoint
- [x] Documentar response model de cada endpoint
- [x] Documentar exemplos básicos quando necessário

## Fase 9: Tratamento de erros

**Status geral:** Parcial

### 9.1 Erros de domínio
- [x] Criar erro para task não encontrada
- [x] Mapear erro de domínio para resposta HTTP
- [ ] Padronizar mensagens de erro

### 9.2 Validação
- [x] Garantir resposta 422 para payload inválido
- [x] Garantir resposta 422 para filtros inválidos
- [x] Garantir consistência entre API e DTOs

### 9.3 Erros inesperados
- [ ] Definir comportamento para falhas de banco
- [ ] Definir comportamento para falhas de conexão
- [ ] Definir retorno em falhas internas

## Fase 10: Testes

**Status geral:** Concluída

### 10.1 Testes de service
- [x] Testar criação de task
- [x] Testar listagem com filtros
- [x] Testar listagem sem resultados
- [x] Testar busca por task inexistente
- [x] Testar atualização de task
- [x] Testar conclusão de task
- [x] Testar reabertura de task
- [x] Testar exclusão de task
- [x] Testar preservação de auditoria após exclusão

### 10.2 Testes de API
- [x] Testar criação via endpoint
- [x] Testar consulta via endpoint
- [x] Testar listagem via endpoint
- [x] Testar atualização via endpoint
- [x] Testar conclusão via endpoint
- [x] Testar reabertura via endpoint
- [x] Testar exclusão via endpoint
- [x] Testar `404` para task inexistente
- [x] Testar `422` para payload inválido

### 10.3 Testes de regressão
- [x] Garantir que novas alterações não quebrem endpoints já existentes
- [x] Garantir que auditoria continue preservada
- [x] Garantir que filtros continuem funcionando

## Fase 11: Documentação

**Status geral:** Concluída

### 11.1 README
- [x] Descrever o objetivo do projeto
- [x] Descrever a stack utilizada
- [x] Descrever os pré-requisitos
- [x] Descrever a configuração do ambiente
- [x] Descrever como executar a aplicação
- [x] Descrever como rodar os testes
- [x] Listar endpoints principais
- [x] Adicionar exemplos de uso

### 11.2 Documentação técnica
- [x] Atualizar documentos de visão
- [x] Atualizar documentos de requisitos
- [x] Atualizar documentos de arquitetura
- [x] Manter os diagramas coerentes com o código
- [x] Registrar decisões importantes do projeto

### 11.3 Diagramas
- [x] Atualizar o diagrama lógico
- [x] Atualizar o diagrama do banco
- [x] Confirmar se os diagramas refletem o estado atual
- [x] Adicionar novos diagramas se a arquitetura crescer

## Fase 12: Qualidade e manutenção

**Status geral:** Parcial

### 12.1 Organização
- [x] Revisar nomes de módulos e classes
- [x] Revisar consistência entre pastas e responsabilidades
- [x] Revisar imports e exports públicos
- [x] Revisar duplicações desnecessárias

### 12.2 Evolução
- [x] Definir estratégia de versionamento da API
- [x] Definir estratégia de paginação futura
- [x] Definir estratégia de autenticação futura
- [x] Definir estratégia de autorização futura
- [x] Definir estratégia de expansão do domínio

### 12.3 Manutenção
- [ ] Revisar backlog periodicamente
- [ ] Atualizar prioridades conforme o projeto evoluir
- [ ] Marcar itens concluídos com evidência no código
- [ ] Remover itens que deixarem de fazer sentido

## Checklist rápido de acompanhamento

Use esta lista para um resumo visual do andamento geral:

- [x] Planejamento definido
- [x] Ambiente preparado
- [x] Estrutura do projeto criada
- [x] Modelagem de dados concluída
- [x] DTOs definidos
- [x] Repositório implementado
- [x] Service layer implementada
- [x] Rotas HTTP implementadas
- [x] Tratamento de erros aplicado
- [x] Testes cobrindo service e API
- [x] Documentação atualizada
- [x] Diagramas atualizados
- [ ] Backlog revisado periodicamente
