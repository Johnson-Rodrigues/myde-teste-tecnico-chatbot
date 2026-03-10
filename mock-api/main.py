"""
Mock API de Pedidos — NovaTech
Simula a API de consulta de pedidos para o teste técnico de Chatbot Developer.
"""

from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import random

app = FastAPI(title="NovaTech Mock API - Pedidos", version="1.0.0")

# Pedidos mock pré-cadastrados
ORDERS = {
    "PED-1001": {
        "order_id": "PED-1001",
        "customer_name": "Maria Silva",
        "status": "em_transito",
        "status_description": "Pedido em trânsito — previsão de entrega: 15/03/2026",
        "items": ["Plano NovaTech Pro — Licença Anual"],
        "total": 1199.90,
        "created_at": "2026-02-20T10:30:00Z",
        "updated_at": "2026-03-05T14:20:00Z",
    },
    "PED-1002": {
        "order_id": "PED-1002",
        "customer_name": "João Santos",
        "status": "entregue",
        "status_description": "Pedido entregue em 01/03/2026",
        "items": ["Plano NovaTech Starter — Licença Mensal", "Treinamento Extra (1h)"],
        "total": 299.90,
        "created_at": "2026-02-15T09:00:00Z",
        "updated_at": "2026-03-01T11:45:00Z",
    },
    "PED-1003": {
        "order_id": "PED-1003",
        "customer_name": "Ana Oliveira",
        "status": "pendente",
        "status_description": "Aguardando confirmação de pagamento",
        "items": ["Plano NovaTech Enterprise — Licença Anual"],
        "total": 7679.04,
        "created_at": "2026-03-08T16:00:00Z",
        "updated_at": "2026-03-08T16:00:00Z",
    },
    "PED-1004": {
        "order_id": "PED-1004",
        "customer_name": "Carlos Ferreira",
        "status": "cancelado",
        "status_description": "Pedido cancelado pelo cliente em 05/03/2026",
        "items": ["Plano NovaTech Pro — Licença Mensal"],
        "total": 299.90,
        "created_at": "2026-03-01T08:30:00Z",
        "updated_at": "2026-03-05T10:15:00Z",
    },
    "PED-1005": {
        "order_id": "PED-1005",
        "customer_name": "Fernanda Lima",
        "status": "confirmado",
        "status_description": "Pagamento confirmado — pedido sendo processado",
        "items": ["Plano NovaTech Pro — Licença Anual", "Treinamento Extra (2h)"],
        "total": 1599.80,
        "created_at": "2026-03-07T14:20:00Z",
        "updated_at": "2026-03-08T09:00:00Z",
    },
    "PED-1006": {
        "order_id": "PED-1006",
        "customer_name": "Roberto Almeida",
        "status": "em_separacao",
        "status_description": "Pedido em separação — será enviado em breve",
        "items": ["Plano NovaTech Enterprise — Licença Mensal"],
        "total": 799.90,
        "created_at": "2026-03-06T11:00:00Z",
        "updated_at": "2026-03-08T08:30:00Z",
    },
}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "NovaTech Mock API - Pedidos", "version": "1.0.0"}


@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    """Consulta um pedido pelo número (formato: PED-XXXX)."""
    order_id = order_id.upper()

    if order_id not in ORDERS:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "order_not_found",
                "message": f"Pedido '{order_id}' não encontrado. Verifique o número e tente novamente.",
            },
        )

    return ORDERS[order_id]


@app.get("/api/orders")
def list_orders():
    """Lista todos os pedidos disponíveis (para debug/testes)."""
    return {"orders": list(ORDERS.values()), "total": len(ORDERS)}
