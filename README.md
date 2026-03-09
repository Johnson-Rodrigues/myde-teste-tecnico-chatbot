# Teste Técnico — Desenvolvedor Chatbot / IA Conversacional

## Sobre a vaga

Você fará parte de uma equipe que desenvolve assistentes virtuais inteligentes para atendimento ao cliente. O dia a dia envolve integração com LLMs, construção de fluxos conversacionais, RAG (Retrieval-Augmented Generation) e orquestração de ferramentas.

Este teste simula um cenário real do dia a dia do projeto.

---

## O Desafio

Construir um **chatbot de FAQ inteligente** para uma empresa fictícia chamada **NovaTech** (SaaS de gestão empresarial). O chatbot deve:

1. **Responder perguntas** usando uma base de conhecimento fornecida (RAG)
2. **Consultar status de pedidos** chamando uma API externa (mock fornecido)
3. **Manter contexto** da conversa (multi-turn)

---

## Contexto de Negócio

A NovaTech recebe centenas de perguntas por dia de seus clientes. O chatbot deve:

```
1. Cliente faz uma pergunta sobre o produto → Bot busca na base de conhecimento e responde
2. Cliente pergunta sobre seu pedido → Bot pede o número do pedido e consulta a API
3. Cliente faz uma pergunta fora do escopo → Bot informa educadamente que não pode ajudar
4. A conversa deve manter contexto entre as mensagens
```

---

## Requisitos Técnicos

### 1. Integração com LLM

- Utilize a API da **OpenAI** (GPT-3.5/4) ou **Anthropic** (Claude) — à sua escolha
- O candidato deve usar sua **própria API key** (ambas oferecem créditos gratuitos para novos cadastros)
- Configure um **system prompt** adequado para o papel de assistente da NovaTech

### 2. RAG — Retrieval-Augmented Generation

Uma pasta `knowledge-base/` é fornecida com 3 documentos sobre a NovaTech. O chatbot deve:

- **Indexar** os documentos ao iniciar (pode usar qualquer estratégia: embeddings, busca por similaridade, keyword search, etc.)
- **Buscar** os trechos mais relevantes quando o usuário faz uma pergunta
- **Injetar** o contexto encontrado no prompt enviado à LLM
- A resposta deve ser baseada **apenas** no conteúdo dos documentos. Se a informação não estiver na base, o bot deve informar que não encontrou a resposta

> Você pode usar bibliotecas como `chromadb`, `faiss`, `langchain`, `llama-index` ou implementar uma solução simples com embeddings + similaridade de cosseno. A escolha é sua.

### 3. Consulta de Pedidos (Function Calling / Tool Use)

O chatbot deve ser capaz de **consultar o status de um pedido** quando o cliente solicitar. Para isso:

- Identifique a intenção do usuário (quer consultar um pedido)
- Extraia ou solicite o **número do pedido** (formato: `PED-XXXX`)
- Chame a **API mock fornecida** para obter o status
- Responda ao cliente com as informações do pedido

A implementação pode usar:
- **Function calling** nativo da API (OpenAI tools / Claude tool_use) — **recomendado**
- Ou parsing manual da resposta da LLM

### 4. Histórico de Conversa

- Mantenha o histórico de mensagens da sessão atual
- A LLM deve receber o contexto das mensagens anteriores para manter coerência
- Não é necessário persistir entre reinícios (in-memory é suficiente)

### 5. Interface

A interface pode ser **uma das seguintes** (escolha do candidato):

- **API REST** com endpoints de chat (mínimo: `POST /chat` recebendo `message` e `session_id`)
- **Interface de terminal** interativa (CLI)
- **Interface web simples** (diferencial, não obrigatório)

---

## Infraestrutura Fornecida

### Mock API de Pedidos

Um servidor mock é fornecido via Docker que simula a API de pedidos da NovaTech:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/orders/{order_id}` | Consulta pedido pelo número (ex: `PED-1001`) |
| GET | `/health` | Health check |

**Exemplo de resposta:**
```json
{
  "order_id": "PED-1001",
  "customer_name": "Maria Silva",
  "status": "em_transito",
  "status_description": "Pedido em trânsito — previsão de entrega: 15/03/2026",
  "items": ["Plano NovaTech Pro — Licença Anual"],
  "total": 1199.90,
  "created_at": "2026-02-20T10:30:00Z",
  "updated_at": "2026-03-05T14:20:00Z"
}
```

**Status possíveis:** `pendente`, `confirmado`, `em_separacao`, `em_transito`, `entregue`, `cancelado`

### Base de Conhecimento

A pasta `knowledge-base/` contém 3 documentos:

| Arquivo | Conteúdo |
|---------|----------|
| `planos-e-precos.md` | Planos, preços e funcionalidades da NovaTech |
| `politica-de-suporte.md` | Política de suporte, SLA e canais de atendimento |
| `faq-geral.md` | Perguntas frequentes sobre a plataforma |

### Docker Compose

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| `mock-api` | 8001 | Mock da API de pedidos da NovaTech |

Para subir:
```bash
docker-compose up -d
```

---

## O que esperamos na entrega

### Obrigatório
- [ ] Código fonte em repositório Git
- [ ] `README.md` com instruções claras para rodar o projeto
- [ ] Integração com LLM funcionando (OpenAI ou Anthropic)
- [ ] RAG buscando nos documentos fornecidos e usando o contexto nas respostas
- [ ] Consulta de pedidos funcionando (via API mock)
- [ ] Histórico de conversa (multi-turn)
- [ ] O bot não inventa informações que não estão na base de conhecimento

### Diferenciais (não obrigatórios)
- [ ] Function calling nativo da API (em vez de parsing manual)
- [ ] Interface web simples
- [ ] Testes unitários
- [ ] Logs estruturados
- [ ] Tratamento de erros e respostas amigáveis quando a API está fora
- [ ] Streaming de respostas

---

## Critérios de Avaliação

| Critério | Peso | O que avaliamos |
|----------|------|-----------------|
| **Qualidade dos prompts** | 30% | System prompt bem elaborado, injeção de contexto, controle de tom e escopo |
| **RAG** | 30% | Indexação, busca relevante, respostas baseadas nos documentos |
| **Function calling / Tools** | 20% | Identificação de intenção, extração de dados, integração com API |
| **Organização do código** | 20% | Estrutura, legibilidade, separação de responsabilidades |

---

## Regras

- Prazo: **3 dias corridos** a partir do recebimento (~2h por dia)
- Linguagem: **Python 3.11+**
- Você pode usar qualquer biblioteca ou framework (LangChain, LlamaIndex, ou implementação manual)
- O candidato deve usar sua **própria API key** da OpenAI ou Anthropic
- O projeto deve funcionar com `docker-compose up` (para o mock) + comando para iniciar o chatbot
- Em caso de dúvidas, documente suas decisões e premissas no README

---

## Como começar

```bash
# 1. Clone este repositório
git clone <url-do-repositorio>

# 2. Suba o mock de pedidos
docker-compose up -d

# 3. Verifique se o mock está rodando
curl http://localhost:8001/health

# 4. Consulte um pedido de exemplo
curl http://localhost:8001/api/orders/PED-1001

# 5. Explore a base de conhecimento em knowledge-base/

# 6. Desenvolva sua solução!
```

Boa sorte!
