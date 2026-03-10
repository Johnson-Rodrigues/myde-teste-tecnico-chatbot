import re

ORDER_ID_RE = re.compile(r"\bPED-\d{4}\b", re.IGNORECASE)


def extract_order_id(text: str) -> str | None:
    m = ORDER_ID_RE.search(text or "")
    return m.group(0).upper() if m else None
