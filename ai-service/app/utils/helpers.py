from datetime import datetime

def format_currency(value: float) -> str:
    return f"{value:,.2f} TL"

def get_current_timestamp() -> str:
    return datetime.now().isoformat()