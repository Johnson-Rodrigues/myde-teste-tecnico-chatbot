from __future__ import annotations

from typing import Any, Dict

import httpx

from .settings import settings


class OrdersClient:
    def __init__(self) -> None:
        self._base_url = settings.mock_api_base_url.rstrip("/")

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        url = f"{self._base_url}/api/orders/{order_id}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)

        if resp.status_code == 404:
            # normalize error
            data = resp.json()
            raise ValueError(data.get("detail", {}).get("message", "Pedido não encontrado"))
        resp.raise_for_status()
        return resp.json()
