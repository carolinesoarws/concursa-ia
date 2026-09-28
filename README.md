# concursa-ia
Sistema de chatbot simples para simular uma prova para concursos. 

## Principal responsabilidade
Esse sistema tem principal responsabilidade de gerar uma pergunta com 4 opções (utilizando um banco de informaçõe em pdf e provas antigas), aguardar pela resposta do usuário, validar se a resposta está correta com base no banco de informações e retornar essa informação para o usuário 

## Arquitetura 

1. Agente de Perguntas 
Este agente é responsável por receber o tema selecionado pelo usuário, gerar as perguntas enviar para o usuário e colher as respostas e salvar.

2. Agente avaliador 
Este agente é responsável por receber a lista de perguntas e respostas feita para o usuário naquela operação validar se está correto com base nno conteúdo e nas respostas e retornar cada pergunta com a correção (certo ou errado) e com a resposta explicando a pergunta. 

3. Agente Juiz
Agente responsável por avaliar a resposta com a pergunta e ter certeza que está correto 

4. Orquestrador
Responsável por orquestrar o tempo de prova, perguntas enviadas para o usuário e respondidas e toda a orquestração do sistema. 

# Concursa IA

Sistema de chatbot baseado em Inteligência Artificial para geração, aplicação e correção de simulados para concursos públicos.

O **Concursa IA** utiliza materiais de estudo, PDFs, editais e provas anteriores como base de conhecimento para gerar questões de múltipla escolha, registrar as respostas do usuário, corrigir o simulado e apresentar explicações fundamentadas no conteúdo utilizado.

---

## 1. Objetivo

O objetivo do sistema é permitir que um usuário realize simulados personalizados a partir de um tema ou matéria de concurso.

O fluxo principal é:

1. O usuário seleciona um tema ou matéria.
2. O usuário define a quantidade de questões.
3. O sistema recupera informações relevantes da base de conhecimento.
4. O sistema gera questões com quatro alternativas.
5. O usuário responde às questões.
6. O sistema registra as respostas.
7. Ao finalizar o simulado, as respostas são avaliadas.
8. Um agente adicional verifica a consistência da correção.
9. O sistema apresenta o resultado final, incluindo explicações para cada questão.

---

# 2. Requisitos Funcionais

## RF01 — Seleção de tema

O sistema deve permitir que o usuário informe o tema ou matéria que deseja estudar.

Exemplos:

- Direito Tributário
- Direito Constitucional
- Português
- Raciocínio Lógico
- Sistema Financeiro Nacional
- Tecnologia da Informação

---

## RF02 — Configuração do simulado

O usuário deve poder configurar o simulado antes de iniciá-lo.

Inicialmente, devem ser suportados:

- tema;
- quantidade de questões;
- tempo de prova.

Futuramente poderão ser adicionados:

- nível de dificuldade;
- banca;
- concurso;
- cargo;
- ano;
- assuntos específicos.

---

## RF03 — Geração de questões

O sistema deve gerar questões de múltipla escolha contendo exatamente quatro alternativas.

Exemplo:

```text
Qual das alternativas representa corretamente o conceito de competência tributária?

A) ...
B) ...
C) ...
D) ...
```

Cada questão deve possuir internamente:

```json
{
  "question": "Texto da questão",
  "alternatives": {
    "A": "Alternativa A",
    "B": "Alternativa B",
    "C": "Alternativa C",
    "D": "Alternativa D"
  },
  "correct_answer": "B",
  "explanation": "Explicação da resposta",
  "sources": []
}
```

A resposta correta e a explicação não devem ser enviadas ao usuário antes da correção.

---

## RF04 — Base de conhecimento

As questões devem ser fundamentadas em uma base de conhecimento formada por documentos como:

- PDFs;
- apostilas;
- legislação;
- editais;
- materiais de estudo;
- provas anteriores;
- gabaritos oficiais.

O sistema não deve depender exclusivamente do conhecimento interno do LLM para determinar a resposta correta.

Sempre que possível, a geração e a correção devem utilizar evidências recuperadas da base de conhecimento.

---

## RF05 — Resposta do usuário

O sistema deve apresentar uma questão por vez e aguardar a resposta do usuário.

Exemplo:

```text
Questão 3/20

[pergunta]

A) ...
B) ...
C) ...
D) ...

Resposta: C
```

A resposta deve ser armazenada junto com a questão correspondente.

---

## RF06 — Controle da prova

Durante a execução do simulado, o sistema deve manter o estado da prova.

Exemplo:

```json
{
  "exam_id": "uuid",
  "status": "IN_PROGRESS",
  "total_questions": 20,
  "current_question": 7,
  "answered_questions": 6,
  "started_at": "...",
  "expires_at": "..."
}
```

O sistema deve saber:

- quais questões foram apresentadas;
- quais foram respondidas;
- qual resposta foi fornecida;
- quanto tempo resta;
- quando a prova foi iniciada;
- quando foi finalizada.

---

## RF07 — Correção

Ao final do simulado, o sistema deve corrigir todas as respostas.

Para cada questão devem ser apresentados:

- pergunta;
- resposta do usuário;
- resposta correta;
- status `CORRETA` ou `INCORRETA`;
- explicação;
- referência utilizada para fundamentar a correção.

Exemplo:

```text
Questão 4

Sua resposta: C
Resposta correta: B

❌ INCORRETA

Explicação:
A competência tributária corresponde...

Fonte:
Material de Direito Tributário, página 32.
```

---

## RF08 — Resultado final

Ao final da correção, o sistema deve apresentar um resumo.

Exemplo:

```text
Resultado

Questões: 20
Acertos: 16
Erros: 4
Aproveitamento: 80%
Tempo utilizado: 42 minutos
```

Futuramente o sistema poderá apresentar métricas por assunto e histórico de evolução.

---

# 3. Arquitetura de Agentes

O sistema será composto inicialmente por quatro componentes principais.

```text
                         ┌───────────────────┐
                         │      Usuário      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Orquestrador    │
                         └─────────┬─────────┘
                                   │
                  ┌────────────────┴────────────────┐
                  │                                 │
                  ▼                                 ▼
        ┌───────────────────┐             ┌──────────────────┐
        │ Agente de         │             │ Base de          │
        │ Perguntas         │◄───────────►│ Conhecimento     │
        └───────────────────┘             │ / RAG            │
                  │                       └──────────────────┘
                  ▼
              Usuário
                  │
                  ▼
        ┌───────────────────┐
        │ Agente Avaliador  │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │   Agente Juiz     │
        └─────────┬─────────┘
                  │
                  ▼
             Resultado
```

---

# 4. Agente de Perguntas

## Responsabilidade

O **Agente de Perguntas** é responsável pela criação das questões do simulado.

Ele recebe informações como:

```json
{
  "topic": "Competência Tributária",
  "number_of_questions": 10
}
```

Antes de gerar uma questão, o agente deve consultar a base de conhecimento.

O contexto recuperado deve servir como fundamento para a criação da pergunta, alternativas, resposta correta e explicação.

## Entrada

- tema;
- quantidade de questões;
- contexto recuperado pelo RAG;
- opcionalmente dificuldade, banca e concurso.

## Saída

Uma estrutura contendo a questão gerada.

```json
{
  "id": "uuid",
  "question": "...",
  "alternatives": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  },
  "correct_answer": "C",
  "explanation": "...",
  "sources": [
    {
      "document_id": "...",
      "page": 10,
      "chunk_id": "..."
    }
  ]
}
```

O agente deve evitar:

- questões ambíguas;
- mais de uma alternativa correta;
- questões sem respaldo documental;
- alternativas obviamente absurdas;
- revelar a resposta correta durante a prova.

---

# 5. Agente Avaliador

## Responsabilidade

O **Agente Avaliador** é responsável pela correção do simulado.

Ao término da prova, ele recebe as questões e as respostas fornecidas pelo usuário.

Exemplo:

```json
{
  "question_id": "123",
  "user_answer": "A"
}
```

O agente compara a resposta fornecida com o gabarito e produz uma explicação.

## Saída

```json
{
  "question_id": "123",
  "user_answer": "A",
  "correct_answer": "C",
  "is_correct": false,
  "explanation": "...",
  "sources": []
}
```

A explicação deve ser fundamentada na base de conhecimento e não apenas no conhecimento interno do modelo.

---

# 6. Agente Juiz

## Responsabilidade

O **Agente Juiz** funciona como uma segunda camada de validação.

Sua função não é gerar uma nova resposta arbitrariamente, mas verificar se a questão e sua correção são consistentes com as evidências recuperadas.

O juiz deve receber:

- pergunta;
- alternativas;
- resposta considerada correta;
- resposta do usuário;
- explicação do avaliador;
- evidências recuperadas da base.

## Saída

```json
{
  "question_id": "123",
  "verdict": "APPROVED",
  "confidence": 0.97,
  "reason": "A resposta C é diretamente suportada pelo trecho recuperado."
}
```

Possíveis resultados:

```text
APPROVED
REVIEW_REQUIRED
INVALID_QUESTION
```

### APPROVED

A correção está de acordo com as evidências.

### REVIEW_REQUIRED

As evidências não são suficientes para validar a correção com segurança.

### INVALID_QUESTION

A questão apresenta algum problema, como ambiguidade ou mais de uma alternativa defensável.

Questões consideradas inválidas não devem prejudicar a pontuação do usuário.

---

# 7. Orquestrador

## Responsabilidade

O **Orquestrador** controla o fluxo completo do simulado.

Ele não deve ser responsável por decidir sozinho o conteúdo das questões ou suas respostas.

Sua função é coordenar os componentes.

Responsabilidades:

- criar uma nova sessão de prova;
- controlar o estado da prova;
- controlar o cronômetro;
- solicitar questões;
- enviar questões ao usuário;
- receber respostas;
- persistir respostas;
- determinar a próxima questão;
- finalizar a prova;
- chamar o Agente Avaliador;
- chamar o Agente Juiz;
- calcular a pontuação;
- montar o resultado final.

Fluxo simplificado:

```text
START
  │
  ▼
Criar sessão
  │
  ▼
Selecionar tema
  │
  ▼
Recuperar contexto
  │
  ▼
Gerar questão
  │
  ▼
Apresentar questão
  │
  ▼
Receber resposta
  │
  ▼
Salvar resposta
  │
  ├──── existem questões restantes? ──── YES ───► próxima questão
  │
  NO
  │
  ▼
Finalizar prova
  │
  ▼
Agente Avaliador
  │
  ▼
Agente Juiz
  │
  ▼
Calcular resultado
  │
  ▼
Apresentar correção
  │
  ▼
END
```

---

# 8. RAG — Retrieval-Augmented Generation

Para reduzir alucinações, o sistema deverá utilizar **RAG**.

Os documentos serão processados e divididos em pequenos trechos (`chunks`).

Fluxo de ingestão:

```text
PDF
 │
 ▼
Extração de texto
 │
 ▼
Limpeza
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Vector Store
```

Durante a geração:

```text
Tema
 │
 ▼
Busca semântica
 │
 ▼
Top K chunks
 │
 ▼
Contexto
 │
 ▼
LLM
 │
 ▼
Questão
```

Isso permite que o LLM receba em runtime os trechos relevantes do material em vez de depender apenas do que foi aprendido durante seu treinamento.

---

# 9. Tipos de documentos

O sistema deverá diferenciar pelo menos dois tipos de documentos.

### Material teórico

Utilizado como fonte de conhecimento:

```text
PDFs
leis
apostilas
editais
material didático
```

### Provas anteriores

Utilizadas como referência para:

```text
formato das questões
nível de dificuldade
estilo da banca
assuntos recorrentes
```

Quando houver gabarito oficial, ele deve ser armazenado junto à questão original.

---

# 10. Modelo de Dados Inicial

## Document

```text
id
filename
document_type
contest
exam_board
year
created_at
```

## DocumentChunk

```text
id
document_id
content
page
embedding
metadata
```

## Exam

```text
id
user_id
topic
status
started_at
finished_at
expires_at
total_questions
score
```

## Question

```text
id
exam_id
question
alternative_a
alternative_b
alternative_c
alternative_d
correct_answer
explanation
source_metadata
```

## UserAnswer

```text
id
question_id
user_answer
answered_at
```

## Evaluation

```text
id
question_id
is_correct
explanation
judge_verdict
judge_confidence
```

---

# 11. Estados da prova

Uma prova poderá possuir os seguintes estados:

```text
CREATED
IN_PROGRESS
FINISHED
EVALUATING
EVALUATED
EXPIRED
```

Fluxo esperado:

```text
CREATED
   │
   ▼
IN_PROGRESS
   │
   ├──── tempo esgotado ───► EXPIRED
   │
   ▼
FINISHED
   │
   ▼
EVALUATING
   │
   ▼
EVALUATED
```

---

# 12. Regras de Negócio

### RN01

Toda questão deve possuir exatamente quatro alternativas.

### RN02

Toda questão deve possuir apenas uma resposta considerada correta.

### RN03

Toda questão gerada deve possuir referência para pelo menos uma evidência da base de conhecimento.

### RN04

A resposta correta não deve ser enviada ao frontend antes da conclusão da prova.

### RN05

Toda resposta do usuário deve ser persistida.

### RN06

Após o encerramento da prova, respostas não poderão ser modificadas.

### RN07

Quando o tempo acabar, a prova deverá ser automaticamente encerrada.

### RN08

Questões classificadas pelo juiz como `INVALID_QUESTION` devem ser anuladas.

### RN09

O cálculo da pontuação deve ser determinístico e realizado pela aplicação, e não pelo LLM.

### RN10

A comparação entre uma alternativa objetiva e o gabarito também deve ser determinística sempre que possível.

O LLM deve ser utilizado principalmente para:

- geração;
- explicação;
- recuperação contextual;
- validação semântica.

---

# 13. Separação entre lógica determinística e IA

Uma regra importante da arquitetura é:

> Não utilizar LLM para tarefas que podem ser resolvidas de maneira determinística.

Por exemplo:

```python
is_correct = user_answer == correct_answer
```

não precisa ser decidido por um agente.

Da mesma maneira:

```text
pontuação
tempo restante
quantidade de acertos
quantidade de erros
estado da prova
```

devem ser controlados pela aplicação.

Os agentes devem atuar onde existe necessidade de interpretação ou geração de linguagem.

---

# 14. Arquitetura Técnica Inicial

Uma possível arquitetura para o MVP:

```text
Frontend
   │
   │ HTTP
   ▼
FastAPI
   │
   ▼
Exam Orchestrator
   │
   ├──────── Question Agent
   │
   ├──────── Evaluation Agent
   │
   ├──────── Judge Agent
   │
   │
   ├──────── RAG Service
   │             │
   │             ▼
   │        Vector Store
   │
   ▼
PostgreSQL
```

Tecnologias possíveis:

```text
Backend:
Python
FastAPI
Pydantic

IA:
LLM
LangGraph

RAG:
Embeddings
Vector Store

Banco:
PostgreSQL

Vector Store:
pgvector ou Qdrant

Frontend:
React

Infra:
Docker
```

Para um MVP, **PostgreSQL + pgvector** pode simplificar a arquitetura, pois dados relacionais e embeddings podem permanecer no mesmo banco.

---

# 15. Estrutura sugerida do backend

```text
concursa-ia/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── exams.py
│   │   ├── questions.py
│   │   └── documents.py
│   │
│   ├── agents/
│   │   ├── question_agent.py
│   │   ├── evaluator_agent.py
│   │   └── judge_agent.py
│   │
│   ├── orchestration/
│   │   ├── exam_graph.py
│   │   └── exam_state.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   └── retrieval.py
│   │
│   ├── models/
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── document.py
│   │
│   ├── schemas/
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── evaluation.py
│   │
│   ├── services/
│   │   ├── exam_service.py
│   │   └── scoring_service.py
│   │
│   └── repositories/
│       ├── exam_repository.py
│       └── document_repository.py
│
├── tests/
│
├── data/
│   ├── materials/
│   └── previous_exams/
│
├── scripts/
│   └── ingest_documents.py
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

---

# 16. API inicial

## Criar prova

```http
POST /exams
```

Request:

```json
{
  "topic": "Competência Tributária",
  "number_of_questions": 10,
  "duration_minutes": 30
}
```

---

## Buscar próxima questão

```http
GET /exams/{exam_id}/questions/next
```

---

## Responder questão

```http
POST /exams/{exam_id}/answers
```

Request:

```json
{
  "question_id": "uuid",
  "answer": "C"
}
```

---

## Finalizar prova

```http
POST /exams/{exam_id}/finish
```

---

## Consultar resultado

```http
GET /exams/{exam_id}/result
```

---

# 17. Observabilidade

Como o sistema utiliza LLMs, deve existir rastreabilidade das operações.

Sempre que possível devem ser registrados:

```text
agent
model
prompt_version
retrieved_chunks
document_ids
latency
token_usage
timestamp
exam_id
question_id
```

Isso será importante para investigar situações como:

```text
"Por que essa questão foi gerada?"

"Qual documento sustentou essa resposta?"

"Por que o juiz aprovou essa correção?"
```

---

# 18. Tratamento de Alucinações

O sistema deve assumir que o LLM pode produzir informações incorretas.

Por isso:

1. questões devem ser fundamentadas em conteúdo recuperado;
2. fontes utilizadas devem ser armazenadas;
3. respostas corretas devem ser vinculadas às evidências;
4. o avaliador deve receber as evidências relevantes;
5. o juiz deve validar a consistência da correção;
6. questões sem evidência suficiente devem ser rejeitadas ou encaminhadas para revisão.

O objetivo não é eliminar completamente alucinações, mas reduzir sua ocorrência e impedir que respostas não fundamentadas sejam tratadas automaticamente como verdade.

---

# 19. MVP

A primeira versão não precisa implementar todas as funcionalidades futuras.

O MVP deverá permitir:

```text
Upload de PDFs
        ↓
Processamento / RAG
        ↓
Usuário escolhe tema
        ↓
Sistema gera 10 questões
        ↓
Usuário responde
        ↓
Respostas são armazenadas
        ↓
Prova é finalizada
        ↓
Sistema corrige
        ↓
Juiz valida
        ↓
Resultado + explicações
```

Não fazem parte obrigatoriamente do primeiro MVP:

- ranking;
- gamificação;
- aplicativo mobile;
- múltiplas bancas;
- dashboard avançado;
- recomendações personalizadas;
- estatísticas históricas complexas.

---

# 20. Evoluções Futuras

Após o MVP, o sistema poderá incluir:

- histórico de simulados;
- dashboard de desempenho;
- identificação dos assuntos com maior índice de erro;
- geração automática de novos simulados com foco nos pontos fracos;
- simulados específicos por banca;
- simulados baseados em concursos específicos;
- diferentes níveis de dificuldade;
- repetição espaçada;
- ranking;
- gamificação;
- recomendação automática de conteúdo;
- plano de estudos baseado nos erros do usuário.

---

# 21. Princípio Central

O Concursa IA deve seguir o princípio:

> **Gerar com IA, fundamentar com dados e validar antes de confiar.**

O LLM é responsável por interpretar e gerar linguagem, enquanto regras objetivas — pontuação, tempo, estados, persistência e comparação de respostas — permanecem sob responsabilidade da aplicação.

Isso mantém o sistema mais previsível, testável e confiável.