


def split_text(text: str, chunk_size: int = 4096) -> list[str]:
    """Split text into chunks of a given size."""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]