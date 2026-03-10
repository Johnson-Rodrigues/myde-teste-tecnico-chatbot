from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from .memory import InMemoryChatHistory
from .orders_client import OrdersClient
from .prompt import SYSTEM_PROMPT
from .rag import SimpleRAG
from .settings import settings
from .utils import extract_order_id

app = FastAPI(title="NovaTech Chatbot API", version="1.0.0")

history = InMemoryChatHistory()
orders_client = OrdersClient()

# knowledge-base is at repo root; inside container we copy repo into /app.
RAG_DIR = os.path.join(os.getcwd(), "knowledge-base")
rag = SimpleRAG(knowledge_base_dir=RAG_DIR)

llm = AsyncOpenAI(api_key=settings.openai_api_key)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class OrderOut(BaseModel):
    order_id: str
    customer_name: str
    status: str
    status_description: str
    items: List[str] = Field(default_factory=list)
    total: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    used_order_tool: bool
    order: Optional[OrderOut] = None


@app.on_event("startup")
async def _startup() -> None:
    # Build RAG index on startup
    if not os.path.isdir(RAG_DIR):
        # allow local runs from chatbot-api/ too
        alt = os.path.abspath(os.path.join(os.getcwd(), "..", "knowledge-base"))
        if os.path.isdir(alt):
            rag.knowledge_base_dir = alt
    await rag.build()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "healthy"}


async def _answer_with_rag(session_id: str, user_message: str) -> str:
    chunks = await rag.retrieve(user_message)

    if not chunks:
        return (
            "Não encontrei essa informação na base de conhecimento da NovaTech. "
            "Você pode reformular a pergunta ou dar mais detalhes?"
        )

    context = "\n\n".join([f"[{c.source}]\n{c.text}" for c in chunks])

    # build messages with short history
    msgs: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.append(
        {
            "role": "system",
            "content": f"BASE DE CONHECIMENTO (trechos relevantes):\n\n{context}",
        }
    )

    for m in history.get(session_id)[-10:]:
        msgs.append({"role": m.role, "content": m.content})

    msgs.append({"role": "user", "content": user_message})

    resp = await llm.chat.completions.create(
        model=settings.openai_model,
        messages=msgs,
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id.strip()
    user_message = request.message.strip()

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    if not user_message:
        raise HTTPException(status_code=400, detail="message is required")

    history.append(session_id, "user", user_message)

    # Order flow:
    # if user message contains PED-XXXX -> fetch order and answer directly
    order_id = extract_order_id(user_message)
    if order_id:
        try:
            order_raw: Dict[str, Any] = await orders_client.get_order(order_id)
            order = OrderOut(**order_raw)
        except ValueError as e:
            answer = str(e)
            history.append(session_id, "assistant", answer)
            return ChatResponse(
                session_id=session_id,
                answer=answer,
                used_order_tool=True,
                order=None,
            )
        except Exception:
            answer = "Tive um problema ao consultar seu pedido agora. Tente novamente em instantes."
            history.append(session_id, "assistant", answer)
            return ChatResponse(
                session_id=session_id,
                answer=answer,
                used_order_tool=True,
                order=None,
            )

        answer = (
            f"Pedido {order.order_id} ({order.customer_name}):\n"
            f"- Status: {order.status}\n"
            f"- Detalhes: {order.status_description}\n"
            f"- Itens: {', '.join(order.items)}\n"
            f"- Total: R$ {order.total}"
        )
        history.append(session_id, "assistant", answer)
        return ChatResponse(
            session_id=session_id,
            answer=answer,
            used_order_tool=True,
            order=order,
        )

    # If user intent seems order-related but no id, ask for it.
    if "pedido" in user_message.lower() or "status" in user_message.lower():
        answer = "Claro! Qual é o número do seu pedido no formato PED-XXXX?"
        history.append(session_id, "assistant", answer)
        return ChatResponse(
            session_id=session_id,
            answer=answer,
            used_order_tool=False,
            order=None,
        )

    answer = await _answer_with_rag(session_id, user_message)
    history.append(session_id, "assistant", answer)
    return ChatResponse(
        session_id=session_id,
        answer=answer,
        used_order_tool=False,
        order=None,
    )
