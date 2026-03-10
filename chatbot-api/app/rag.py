from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from openai import AsyncOpenAI

from .settings import settings


@dataclass
class DocChunk:
    source: str
    text: str
    embedding: np.ndarray


class SimpleRAG:
    """
    Minimal RAG:
    - load markdown files from knowledge-base/
    - chunk by paragraphs
    - embed chunks with OpenAI embeddings
    - retrieve top-k by cosine similarity
    """

    def __init__(self, knowledge_base_dir: str) -> None:
        self.knowledge_base_dir = knowledge_base_dir
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._chunks: List[DocChunk] = []
        self._ready = False

    async def build(self) -> None:
        files = []
        for name in os.listdir(self.knowledge_base_dir):
            if name.endswith(".md"):
                files.append(os.path.join(self.knowledge_base_dir, name))

        texts: List[Tuple[str, str]] = []
        for path in sorted(files):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            # paragraph chunks
            for para in [p.strip() for p in content.split("\n\n") if p.strip()]:
                texts.append((os.path.basename(path), para))

        if not texts:
            self._chunks = []
            self._ready = True
            return

        embeddings = await self._embed([t[1] for t in texts])
        self._chunks = [
            DocChunk(source=texts[i][0], text=texts[i][1], embedding=embeddings[i])
            for i in range(len(texts))
        ]
        self._ready = True

    async def _embed(self, inputs: List[str]) -> List[np.ndarray]:
        resp = await self._client.embeddings.create(
            model=settings.openai_embedding_model,
            input=inputs,
        )
        vectors = [np.array(item.embedding, dtype=np.float32) for item in resp.data]
        return vectors

    def _cosine(self, a: np.ndarray, b: np.ndarray) -> float:
        denom = (np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    async def retrieve(self, query: str, top_k: int | None = None) -> List[DocChunk]:
        if not self._ready:
            raise RuntimeError("RAG not built. Call build() on startup.")
        if not self._chunks:
            return []

        top_k = top_k or settings.rag_top_k
        q_emb = (await self._embed([query]))[0]

        scored = [(self._cosine(q_emb, c.embedding), c) for c in self._chunks]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]
