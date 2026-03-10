from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional

Role = Literal["system", "user", "assistant"]


@dataclass
class Message:
    role: Role
    content: str


class InMemoryChatHistory:
    """
    Simple per-session in-memory history.
    Not persisted between restarts (as required).
    """

    def __init__(self) -> None:
        self._store: Dict[str, List[Message]] = {}

    def get(self, session_id: str) -> List[Message]:
        return list(self._store.get(session_id, []))

    def append(self, session_id: str, role: Role, content: str) -> None:
        self._store.setdefault(session_id, []).append(Message(role=role, content=content))

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)
