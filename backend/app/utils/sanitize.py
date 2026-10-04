import re

def sanitize_filename(filename: str) -> str:
    """Sanitize string to be safe for filenames while preserving extension."""
    # Allow alphanumeric, hyphen, underscore, and dot for file extension
    clean = re.sub(r'[^\w\s.-]', '', filename).strip()
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean[:100] or "file"
