# Vision Document

## Produto
TaskFlow API — Micro-API de Gerenciamento de Tarefas

## 1. Problema
Usuários individuais e estudantes frequentemente utilizam métodos informais para organizar tarefas, gerando baixa visibilidade sobre pendências, prioridades e progresso. Em contexto acadêmico, também existe demanda por projetos backend que demonstrem boas práticas modernas sem complexidade excessiva.

## 2. Público-Alvo
### Primário
- Estudantes e profissionais que precisam organizar tarefas pessoais
- Professores avaliadores de projetos técnicos
- Desenvolvedores iniciantes estudando APIs REST

### Secundário
- Pequenas equipes acadêmicas
- Desenvolvedores frontend que precisem consumir uma API simples

## 3. Stakeholders
- Aluno responsável pelo projeto
- Professor/orientador
- Usuários finais
- Instituição de ensino
- Desenvolvedores consumidores da API

## 4. Proposta de Valor
Oferecer uma API simples, confiável e bem estruturada para gerenciamento de tarefas, servindo como solução funcional e demonstração técnica de desenvolvimento backend moderno.

## 5. Visão do Produto
Uma micro-API construída em Python/FastAPI que centraliza criação, consulta, atualização, conclusão e exclusão de tarefas com persistência em PostgreSQL e documentação automática.

## 6. Funcionalidades Principais (Alto Nível)
- Criar tarefas
- Listar tarefas
- Consultar tarefa por ID
- Atualizar tarefas
- Excluir tarefas
- Marcar como concluída
- Reabrir tarefas
- Filtrar por status, prioridade e texto
- Documentação Swagger/OpenAPI

## 7. Diferencial Competitivo
- Simplicidade com qualidade profissional
- Stack moderna e performática
- Estrutura preparada para futura expansão
- Excelente valor acadêmico e de portfólio

## 8. Objetivos de Negócio
- Entregar MVP acadêmico sólido
- Demonstrar domínio técnico em backend Python
- Produzir base reutilizável para projetos futuros
- Maximizar qualidade de entrega e avaliação

## 9. Métricas de Sucesso
- 100% dos endpoints previstos operacionais
- Baixa taxa de erro
- Respostas rápidas em ambiente local
- Código organizado e documentado
- Boa avaliação acadêmica

## 10. Monetização
Fora do escopo atual. Em evolução futura, poderia adotar modelo freemium ou assinatura para equipes.

## 11. Restrições
- Projeto acadêmico individual
- Deploy local
- Sem Docker no MVP
- Sem autenticação no MVP
- Prazo limitado

## 12. Assumptions
- Simplicidade e qualidade serão mais valorizadas que alta complexidade
- PostgreSQL atende plenamente o MVP
- FastAPI é adequado para produtividade e clareza

## 13. Riscos
- Projeto ser percebido como CRUD simples se mal apresentado
- Falta de testes/documentação reduzir nota
- Escopo crescer além do prazo

## 14. Glossário
- API: Interface entre sistemas
- REST: Padrão baseado em HTTP
- CRUD: Criar, Ler, Atualizar e Excluir
- MVP: Produto mínimo viável
- Endpoint: rota funcional da API
- PostgreSQL: banco relacional open source

## 15. Ambiguidades e Próximos Passos
### Decisões Confirmadas
- PostgreSQL
- Deploy local
- Sem Docker
- Sem autenticação no MVP

### Próximos Passos
1. Definir backlog técnico
2. Implementar estrutura base
3. Criar banco e models
4. Implementar endpoints
5. Criar testes
6. Documentar entrega