import os
import pytest

from chatbot_api.app.rag import SimpleRAG


@pytest.mark.asyncio
async def test_rag_build_empty(tmp_path):
    rag = SimpleRAG(str(tmp_path))
    await rag.build()
    chunks = await rag.retrieve("qualquer coisa")
    assert chunks == []
