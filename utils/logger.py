def sanitize_headers(headers: dict[str, str]) -> dict[str, str]:
    """Mask authorization and cookie values for secure logging."""
    sanitized = headers.copy()
    for key in sanitized:
        if key.lower() in ("authorization", "cookie", "x-api-key"):
            val = sanitized[key]
            if len(val) > 12:
                sanitized[key] = f"{val[:6]}...***...{val[-4:]}"
            else:
                sanitized[key] = "***MASKED***"
    return sanitized
