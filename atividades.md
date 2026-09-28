# Concursa IA — Plano de Desenvolvimento

## 1. Objetivo deste documento

Este documento descreve as tarefas necessárias para construir o MVP do **Concursa IA**.

Cada tarefa contém:

- **Objetivo:** por que a tarefa existe.
- **O que fazer:** atividades necessárias.
- **Entregável:** o que precisa existir ao finalizar.
- **Critério de aceite:** como saber que a tarefa realmente terminou.

A implementação deve ser incremental. Uma task só deve ser considerada concluída quando seus critérios de aceite forem atendidos.

---

# ÉPICO 1 — Fundação do Projeto

## TASK 1 — Criar o repositório e estrutura inicial

### Objetivo

Criar a fundação do backend do Concursa IA.

### O que fazer

Criar projeto Python.

Estruturar inicialmente:

```text
concursa-ia/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── agents/
│   ├── orchestration/
│   ├── rag/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── repositories/
│
├── tests/
├── data/
│   ├── materials/
│   └── previous_exams/
│
├── scripts/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Configurar:

- Python;
- ambiente virtual;
- FastAPI;
- Uvicorn;
- Pydantic;
- pytest.

### Entregável

Projeto Python executável com FastAPI.

Executar:

```bash
uvicorn app.main:app --reload
```

deve iniciar a aplicação.

### Critério de aceite

Acessar:

```text
GET /health
```

deve retornar:

```json
{
  "status": "ok"
}
```

---

# ÉPICO 2 — Domínio do Simulado

## TASK 2 — Modelar as entidades principais

### Objetivo

Definir as estruturas utilizadas pelo sistema antes de introduzir IA.

### O que fazer

Criar modelos para:

- Exam;
- Question;
- UserAnswer;
- Evaluation;
- Document;
- DocumentChunk.

Definir os estados:

```text
CREATED
IN_PROGRESS
FINISHED
EVALUATING
EVALUATED
EXPIRED
```

Criar enums para informações controladas, como:

```text
ExamStatus
AnswerOption
JudgeVerdict
DocumentType
```

### Entregável

Modelos do domínio definidos e importáveis pela aplicação.

### Critério de aceite

Deve ser possível representar em Python:

```text
Exam
 ├── Questions
 │     └── Alternatives
 │
 └── UserAnswers
```

sem depender ainda de banco de dados ou LLM.

---

## TASK 3 — Criar schemas Pydantic

### Objetivo

Definir contratos claros entre API e aplicação.

### O que fazer

Criar schemas para:

```text
CreateExamRequest
ExamResponse

QuestionResponse

SubmitAnswerRequest
SubmitAnswerResponse

EvaluationResponse
ExamResultResponse
```

Garantir validações.

Exemplo:

```json
{
  "topic": "Direito Tributário",
  "number_of_questions": 10,
  "duration_minutes": 30
}
```

Não aceitar:

```json
{
  "number_of_questions": -5
}
```

### Entregável

Schemas Pydantic com validação automática.

### Critério de aceite

Requests inválidos devem resultar em erro `422`.

---

# ÉPICO 3 — Primeiro Simulado sem IA

> O objetivo deste épico é fazer o fluxo inteiro funcionar antes de adicionar LLM ou RAG.

## TASK 4 — Criar serviço de prova

### Objetivo

Implementar as regras principais do simulado.

### O que fazer

Criar:

```text
ExamService
```

Responsabilidades:

- criar prova;
- iniciar prova;
- recuperar prova;
- recuperar questão atual;
- registrar resposta;
- avançar questão;
- finalizar prova.

Inicialmente utilizar armazenamento em memória.

### Entregável

Fluxo de prova funcionando sem banco e sem IA.

### Critério de aceite

Deve ser possível:

```text
criar prova
   ↓
responder questão
   ↓
responder próxima
   ↓
finalizar prova
```

---

## TASK 5 — Criar banco de questões mock

### Objetivo

Permitir testar o sistema antes da integração com IA.

### O que fazer

Criar aproximadamente 10 questões fixas.

Exemplo:

```python
QUESTIONS = [...]
```

Cada questão deve possuir:

```text
question
alternatives
correct_answer
explanation
```

### Entregável

Banco mockado de questões.

### Critério de aceite

Uma prova pode ser executada completamente utilizando somente questões mockadas.

---

## TASK 6 — Criar API de provas

### Objetivo

Expor o fluxo através de HTTP.

### O que fazer

Criar endpoints:

```text
POST /exams

GET /exams/{exam_id}

GET /exams/{exam_id}/questions/next

POST /exams/{exam_id}/answers

POST /exams/{exam_id}/finish

GET /exams/{exam_id}/result
```

### Entregável

API funcional.

### Critério de aceite

O fluxo completo deve ser executável pelo Swagger em:

```text
/docs
```

---

# ÉPICO 4 — Correção Determinística

## TASK 7 — Implementar ScoringService

### Objetivo

Separar cálculo de pontuação da Inteligência Artificial.

### O que fazer

Criar:

```text
ScoringService
```

Responsável por:

```python
user_answer == correct_answer
```

Calcular:

```text
total_questions
correct_answers
wrong_answers
invalid_questions
score_percentage
```

### Entregável

Serviço determinístico de correção.

### Critério de aceite

Para:

```text
10 questões
8 corretas
2 erradas
```

o resultado deve retornar:

```text
80%
```

sem utilizar LLM.

---

## TASK 8 — Criar testes do fluxo de prova

### Objetivo

Garantir que as regras básicas não sejam quebradas quando IA e banco forem introduzidos.

### O que fazer

Testar:

- criação de prova;
- resposta válida;
- alternativa inválida;
- tentativa de responder duas vezes;
- finalização;
- cálculo da pontuação;
- tentativa de responder prova finalizada.

### Entregável

Suite inicial de testes automatizados.

### Critério de aceite

Executar:

```bash
pytest
```

e todos os testes devem passar.

---

# ÉPICO 5 — Persistência

## TASK 9 — Configurar PostgreSQL

### Objetivo

Substituir armazenamento em memória por persistência real.

### O que fazer

Configurar PostgreSQL.

Criar conexão utilizando SQLAlchemy.

Configurar migrations com Alembic.

Adicionar variáveis:

```text
DATABASE_URL
```

### Entregável

Aplicação conectada ao PostgreSQL.

### Critério de aceite

Aplicação consegue:

- conectar;
- criar registros;
- consultar registros.

---

## TASK 10 — Persistir provas e respostas

### Objetivo

Fazer com que simulados sobrevivam ao restart da aplicação.

### O que fazer

Criar tabelas para:

```text
exams
questions
user_answers
evaluations
```

Criar repositories.

Exemplo:

```text
ExamRepository
QuestionRepository
AnswerRepository
```

### Entregável

Fluxo do simulado persistido no PostgreSQL.

### Critério de aceite

Criar uma prova, reiniciar a aplicação e recuperar a mesma prova.

---

# ÉPICO 6 — Ingestão de Documentos

## TASK 11 — Criar upload de PDFs

### Objetivo

Permitir adicionar materiais de estudo.

### O que fazer

Criar endpoint:

```text
POST /documents
```

Aceitar arquivos PDF.

Registrar:

```text
filename
document_type
contest
exam_board
year
```

### Entregável

Upload de PDFs funcional.

### Critério de aceite

Enviar um PDF pela API e recuperar seus metadados posteriormente.

---

## TASK 12 — Implementar extração de texto

### Objetivo

Transformar PDF em conteúdo utilizável pelo RAG.

### O que fazer

Implementar:

```text
PDF
 ↓
Text Extraction
 ↓
Clean Text
```

Preservar sempre que possível:

```text
document_id
page
content
```

### Entregável

Serviço capaz de extrair texto de PDF.

### Critério de aceite

Fornecer um PDF e receber seu conteúdo separado por páginas.

---

## TASK 13 — Implementar chunking

### Objetivo

Dividir documentos em trechos menores recuperáveis pelo sistema.

### O que fazer

Criar `ChunkingService`.

Transformar:

```text
Documento
```

em:

```text
Chunk 1
Chunk 2
Chunk 3
...
```

Cada chunk deve manter metadata:

```json
{
  "document_id": "...",
  "page": 32,
  "chunk_index": 5
}
```

### Entregável

Lista de `DocumentChunk`.

### Critério de aceite

Um documento grande deve gerar múltiplos chunks sem perder sua referência ao documento e página original.

---

# ÉPICO 7 — Embeddings e Busca Vetorial

## TASK 14 — Configurar pgvector

### Objetivo

Adicionar busca semântica ao PostgreSQL.

### O que fazer

Instalar extensão:

```text
pgvector
```

Adicionar coluna de embedding aos chunks.

### Entregável

Tabela `document_chunks` com suporte a vetores.

### Critério de aceite

Embeddings podem ser persistidos e consultados.

---

## TASK 15 — Gerar embeddings

### Objetivo

Converter chunks em representações vetoriais.

### O que fazer

Implementar:

```text
EmbeddingService
```

Fluxo:

```text
Chunk
 ↓
Embedding Model
 ↓
Vector
 ↓
PostgreSQL
```

### Entregável

Pipeline de embeddings.

### Critério de aceite

Ao processar um PDF, todos os chunks devem possuir embeddings armazenados.

---

## TASK 16 — Implementar Retriever

### Objetivo

Encontrar conteúdo relevante para um tema.

### O que fazer

Criar:

```text
RetrieverService
```

Entrada:

```text
"competência tributária"
```

Saída:

```text
Top K chunks mais relevantes
```

### Entregável

Busca semântica funcionando.

### Critério de aceite

Uma consulta deve retornar chunks semanticamente relacionados ao assunto solicitado.

---

# ÉPICO 8 — Primeiro RAG

## TASK 17 — Criar pipeline RAG

### Objetivo

Unir retrieval e LLM.

### O que fazer

Implementar:

```text
Pergunta/Tema
      ↓
Embedding
      ↓
Retriever
      ↓
Top K chunks
      ↓
Prompt
      ↓
LLM
```

### Entregável

RAG Service funcional.

### Critério de aceite

O sistema consegue responder uma pergunta utilizando exclusivamente contexto recuperado dos documentos.

---

## TASK 18 — Implementar referências

### Objetivo

Permitir rastrear de onde uma informação veio.

### O que fazer

Toda resposta do RAG deve manter:

```text
document_id
page
chunk_id
```

### Entregável

Sistema de referências.

### Critério de aceite

Para qualquer contexto enviado ao LLM deve ser possível identificar o documento e página de origem.

---

# ÉPICO 9 — Agente de Perguntas

## TASK 19 — Criar Question Agent

### Objetivo

Gerar questões automaticamente.

### O que fazer

Criar agente que recebe:

```text
tema
+
contexto recuperado
```

e retorna:

```json
{
  "question": "...",
  "alternatives": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  },
  "correct_answer": "B",
  "explanation": "...",
  "sources": []
}
```

Utilizar structured output.

### Entregável

Question Agent.

### Critério de aceite

O agente sempre deve retornar uma estrutura válida contendo quatro alternativas.

---

## TASK 20 — Validar questões geradas

### Objetivo

Evitar questões estruturalmente inválidas.

### O que fazer

Validar automaticamente:

```text
4 alternativas?
resposta pertence a A/B/C/D?
pergunta vazia?
explicação vazia?
possui source?
```

Questões inválidas devem ser rejeitadas.

### Entregável

Question Validator.

### Critério de aceite

Uma questão malformada nunca deve chegar ao usuário.

---

## TASK 21 — Integrar Question Agent ao simulado

### Objetivo

Remover as questões mockadas.

### O que fazer

Alterar:

```text
ExamService
```

para solicitar questões ao Question Agent.

### Entregável

Simulado gerado dinamicamente.

### Critério de aceite

Usuário informa:

```text
Direito Tributário
10 questões
```

e recebe 10 questões geradas a partir dos materiais.

---

# ÉPICO 10 — Agente Avaliador

## TASK 22 — Criar Evaluator Agent

### Objetivo

Gerar explicações pedagógicas para a correção.

### O que fazer

Receber:

```text
question
user_answer
correct_answer
sources
```

Gerar:

```text
explanation
```

A explicação deve demonstrar:

- por que a alternativa correta está correta;
- por que a resposta do usuário está incorreta, quando aplicável;
- evidência utilizada.

### Entregável

Evaluator Agent.

### Critério de aceite

Cada questão corrigida deve possuir uma explicação fundamentada.

---

# ÉPICO 11 — Agente Juiz

## TASK 23 — Criar Judge Agent

### Objetivo

Validar questão, gabarito e explicação.

### O que fazer

Receber:

```text
question
alternatives
correct_answer
explanation
evidence
```

Retornar:

```json
{
  "verdict": "APPROVED",
  "confidence": 0.95,
  "reason": "..."
}
```

Possíveis estados:

```text
APPROVED
REVIEW_REQUIRED
INVALID_QUESTION
```

### Entregável

Judge Agent.

### Critério de aceite

O agente deve produzir sempre um dos três estados permitidos.

---

## TASK 24 — Implementar anulação de questões

### Objetivo

Não prejudicar o usuário quando uma questão gerada for considerada inválida.

### O que fazer

Se:

```text
judge_verdict == INVALID_QUESTION
```

a questão deve ser removida do cálculo da nota.

### Entregável

Regra de anulação.

### Critério de aceite

Uma questão inválida não deve ser contabilizada como erro.

---

# ÉPICO 12 — Orquestração

## TASK 25 — Modelar ExamState

### Objetivo

Criar o estado compartilhado pelo workflow.

### O que fazer

Definir estrutura contendo:

```text
exam_id
topic
questions
answers
current_question
retrieved_context
evaluations
judge_results
status
```

### Entregável

Modelo `ExamState`.

### Critério de aceite

Todos os dados necessários para executar uma prova devem poder ser representados pelo estado.

---

## TASK 26 — Criar workflow com LangGraph

### Objetivo

Orquestrar os agentes explicitamente.

### O que fazer

Criar nodes semelhantes a:

```text
retrieve_context
      ↓
generate_question
      ↓
validate_question
      ↓
wait_for_answer
      ↓
save_answer
      ↓
next_question?
      ↓
evaluate_answers
      ↓
judge_evaluations
      ↓
calculate_score
      ↓
finish_exam
```

### Entregável

Graph do Concursa IA.

### Critério de aceite

Uma prova inteira consegue percorrer o workflow corretamente.

---

## TASK 27 — Implementar controle de tempo

### Objetivo

Adicionar duração real ao simulado.

### O que fazer

Armazenar:

```text
started_at
expires_at
finished_at
```

Antes de aceitar respostas verificar:

```text
current_time < expires_at
```

### Entregável

Controle de tempo.

### Critério de aceite

Uma prova expirada não aceita novas respostas.

---

# ÉPICO 13 — Resultado

## TASK 28 — Criar resultado detalhado

### Objetivo

Entregar ao usuário uma correção completa.

### O que fazer

Retornar:

```text
total
acertos
erros
anuladas
percentual
tempo utilizado
```

Para cada questão:

```text
pergunta
resposta do usuário
resposta correta
status
explicação
fontes
```

### Entregável

Endpoint:

```text
GET /exams/{exam_id}/result
```

### Critério de aceite

Resultado completo pode ser consultado após o término da prova.

---

# ÉPICO 14 — Observabilidade

## TASK 29 — Implementar logging estruturado

### Objetivo

Permitir investigação do comportamento da aplicação.

### O que fazer

Registrar:

```text
exam_id
question_id
agent
model
latency
status
timestamp
```

Nunca registrar informações sensíveis desnecessariamente.

### Entregável

Logs estruturados.

### Critério de aceite

É possível acompanhar nos logs o fluxo completo de uma prova.

---

## TASK 30 — Registrar execução dos LLMs

### Objetivo

Entender custo e comportamento dos agentes.

### O que fazer

Registrar quando disponível:

```text
model
prompt_version
input_tokens
output_tokens
latency
retrieved_chunks
```

### Entregável

Tracing básico das operações de IA.

### Critério de aceite

É possível identificar quanto cada etapa de IA consumiu e quais documentos foram utilizados.

---

# ÉPICO 15 — Qualidade

## TASK 31 — Testes unitários

### Objetivo

Testar componentes isoladamente.

### O que fazer

Criar testes para:

```text
ExamService
ScoringService
ChunkingService
RetrieverService
QuestionValidator
```

### Entregável

Suite de testes unitários.

### Critério de aceite

Todos os testes passam com:

```bash
pytest
```

---

## TASK 32 — Testes de integração

### Objetivo

Testar comunicação entre componentes.

### O que fazer

Testar:

```text
API → Service → Database

PDF → Chunk → Embedding → Retriever

Retriever → Question Agent

Exam → Evaluation → Judge
```

### Entregável

Testes de integração.

### Critério de aceite

Os principais fluxos entre componentes possuem cobertura automatizada.

---

## TASK 33 — Teste End-to-End

### Objetivo

Validar o produto completo.

### Cenário

Executar:

```text
Upload PDF
    ↓
Processar documento
    ↓
Criar prova
    ↓
Selecionar tema
    ↓
Gerar questões
    ↓
Responder
    ↓
Finalizar
    ↓
Corrigir
    ↓
Judge
    ↓
Resultado
```

### Entregável

Teste E2E do fluxo principal.

### Critério de aceite

O cenário completo funciona sem intervenção manual no backend.

---

# ÉPICO 16 — Containerização

## TASK 34 — Criar Dockerfile

### Objetivo

Executar a API de maneira reproduzível.

### O que fazer

Criar imagem da aplicação Python.

### Entregável

`Dockerfile`.

### Critério de aceite

Executar a aplicação dentro de um container.

---

## TASK 35 — Criar Docker Compose

### Objetivo

Subir a infraestrutura local com um comando.

### O que fazer

Configurar:

```text
API
PostgreSQL
pgvector
```

### Entregável

`docker-compose.yml`.

### Critério de aceite

Executar:

```bash
docker compose up
```

deve iniciar toda a infraestrutura necessária.

---

# ÉPICO 17 — Documentação

## TASK 36 — Finalizar README

### Objetivo

Permitir que outra pessoa consiga executar e compreender o projeto.

### O que fazer

Documentar:

```text
objetivo
arquitetura
pré-requisitos
instalação
variáveis de ambiente
execução
Docker
endpoints
RAG
agentes
testes
```

### Entregável

README final.

### Critério de aceite

Uma pessoa que nunca viu o projeto consegue executá-lo seguindo apenas o README.

---

# ÉPICO 18 — MVP

## TASK 37 — Validar MVP

O MVP será considerado entregue quando o seguinte fluxo estiver funcionando:

```text
                ┌──────────────┐
                │ Upload PDF   │
                └──────┬───────┘
                       ▼
                 Extract Text
                       │
                       ▼
                    Chunks
                       │
                       ▼
                  Embeddings
                       │
                       ▼
                   pgvector
                       │
                       ▼
                ┌──────────────┐
                │ Criar Prova  │
                └──────┬───────┘
                       ▼
                 Selecionar Tema
                       │
                       ▼
                    RAG
                       │
                       ▼
               Question Agent
                       │
                       ▼
                   Pergunta
                       │
                       ▼
                Resposta Usuário
                       │
                       ▼
                 Persistência
                       │
                 próxima questão
                       │
                       ▼
                 Finalizar Prova
                       │
                       ▼
                 ScoringService
                       │
                       ▼
                Evaluator Agent
                       │
                       ▼
                  Judge Agent
                       │
                       ▼
                   Resultado
```

### Entregável final do MVP

Uma aplicação capaz de:

- receber documentos PDF;
- indexar seu conteúdo;
- realizar busca semântica;
- gerar questões baseadas nos documentos;
- executar um simulado;
- controlar respostas;
- controlar tempo;
- persistir o estado;
- corrigir respostas;
- explicar as respostas;
- validar questões com um Judge;
- apresentar pontuação;
- apresentar referências;
- manter rastreabilidade das operações de IA.

---

# Ordem de Implementação

A ordem recomendada é:

```text
01 → Fundação
02 → Modelagem
03 → Schemas
04 → ExamService
05 → Questões Mock
06 → API
07 → Scoring
08 → Testes

──────── PRIMEIRO MARCO ────────

09 → PostgreSQL
10 → Persistência

──────── SEGUNDO MARCO ─────────

11 → PDF Upload
12 → PDF Extraction
13 → Chunking
14 → pgvector
15 → Embeddings
16 → Retriever

──────── TERCEIRO MARCO ────────

17 → RAG
18 → Sources

──────── QUARTO MARCO ──────────

19 → Question Agent
20 → Question Validator
21 → Integração

──────── QUINTO MARCO ──────────

22 → Evaluator
23 → Judge
24 → Anulação

──────── SEXTO MARCO ───────────

25 → ExamState
26 → LangGraph
27 → Timer
28 → Result

──────── SÉTIMO MARCO ──────────

29 → Logging
30 → LLM Tracing
31 → Unit Tests
32 → Integration Tests
33 → E2E
34 → Docker
35 → Docker Compose
36 → README
37 → MVP Validation
```

---

# Estratégia de Desenvolvimento

Existe uma regra importante para este projeto:

> **Não começar pela IA.**

O primeiro objetivo deve ser construir um sistema de prova completamente funcional usando questões mockadas.

Portanto, o primeiro marco real é:

```text
FastAPI
   ↓
Criar prova
   ↓
Questões Mock
   ↓
Responder
   ↓
Salvar resposta
   ↓
Finalizar
   ↓
Corrigir
   ↓
Resultado
```

Somente depois desse fluxo estar funcionando devem entrar:

```text
PostgreSQL
    ↓
PDF
    ↓
RAG
    ↓
LLM
    ↓
Agents
    ↓
LangGraph
```

Isso permite distinguir problemas de **engenharia de software** de problemas de **IA**.

Se uma prova não finaliza corretamente, por exemplo, será possível saber que o problema está no domínio/orquestração e não no comportamento de um LLM.

---

# Definition of Done

Uma task só pode ser marcada como:

```text
DONE
```

quando:

- implementação concluída;
- código executando;
- critério de aceite atendido;
- testes relevantes passando;
- código commitado;
- documentação atualizada quando necessário.

O fato de "o código estar escrito" não significa que a task está concluída.

---

# Primeiro objetivo

Não pensar inicialmente em:

> "Preciso construir um sistema multiagente com RAG."

Pensar em:

> "Preciso construir uma API que consiga executar corretamente uma prova de 10 questões."

Quando isso funcionar, o sistema será evoluído incrementalmente até que as questões deixem de ser mockadas e passem a ser produzidas pelo pipeline de IA.

Essa será a base sobre a qual todo o Concursa IA será construído.