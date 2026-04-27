# Documento Preparatório para Futuro SRS (Não é SRS)

## Objetivo
Consolidar informações já levantadas e registrar decisões, áreas abertas e insumos que facilitarão a criação futura de um SRS formal.

## 1. Escopo Funcional Confirmado
### Entidade Principal: Task
Campos conceituais já identificados:
- id
- title
- description
- completed
- priority
- created_at
- updated_at
- due_date (opcional)

### Capacidades previstas
- Cadastro de tarefa
- Consulta unitária e listagem
- Atualização total/parcial
- Exclusão
- Conclusão e reabertura
- Filtros de consulta

## 2. Regras de Negócio já Identificadas
- Toda tarefa deve possuir título válido
- Tarefa concluída pode ser reaberta
- Exclusão remove registro logicamente ou fisicamente (decisão pendente)
- Datas devem ser registradas automaticamente
- Filtros não devem alterar dados

## 3. Requisitos Não Funcionais Indicativos
- API responsiva em ambiente local
- Código modular e legível
- Tratamento consistente de erros
- Documentação automática acessível
- Facilidade de manutenção

## 4. Estrutura Técnica Pretendida
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy ou equivalente ORM
- Pydantic para validação
- Pytest para testes

## 5. Endpoints Mapeados para Detalhamento Futuro
- POST /tasks
- GET /tasks
- GET /tasks/{id}
- PUT /tasks/{id}
- PATCH /tasks/{id}/complete
- PATCH /tasks/{id}/reopen
- DELETE /tasks/{id}

## 6. Itens que Futuro SRS Deverá Especificar
- Contratos completos de request/response
- Códigos HTTP por cenário
- Validações de campos
- Regras de paginação
- Ordenação detalhada
- Estratégia de exclusão lógica/física
- Mensagens de erro padronizadas
- Critérios de aceite por endpoint
- Limites de performance

## 7. Itens Fora do MVP Atual
- Autenticação/autorização
- Multiusuário
- Categorias/etiquetas avançadas
- Notificações
- Dashboard visual
- Deploy em cloud
- Docker

## 8. Riscos Técnicos para Mitigação no Futuro SRS
- Crescimento sem versionamento de API
- Falta de padronização de respostas
- Baixa cobertura de testes
- Mudanças de escopo tardias

## 9. Sugestão de Ordem de Implementação
1. Estrutura do projeto
2. Conexão PostgreSQL
3. Modelagem Task
4. CRUD base
5. Filtros e regras extras
6. Testes
7. Revisão final e documentação

## 10. Perguntas em Aberto para Próxima Fase
- Prioridade terá níveis fixos?
- due_date será obrigatório em algum cenário?
- Haverá paginação desde o MVP?
- Exclusão lógica será necessária?
- Haverá versionamento /v1?