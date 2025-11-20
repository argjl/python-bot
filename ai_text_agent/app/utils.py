# app/utils.py

def sanitize_markdown(text: str) -> str:
    """
    Minimal sanitizer for Markdown-like output (safe for the web response).
    You can expand this later for channels like Telegram or HTML.
    """
    return text.replace("\r", "").strip()

def guard_length(text: str, max_len: int = 4096) -> str:
    """
    Limits the reply length so clients don't reject oversized messages.
    """
    return text[:max_len]