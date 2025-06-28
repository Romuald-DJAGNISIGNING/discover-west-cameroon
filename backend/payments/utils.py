from decimal import Decimal

def calculate_platform_fee(amount, percentage=0.10):
    """Calculate the platform (admin) fee from a given amount and fee percentage."""
    return round(Decimal(amount) * Decimal(percentage), 2)

def generate_reference(prefix="TX"):
    """Generate a unique payment reference string."""
    import uuid
    return f"{prefix}-{uuid.uuid4().hex[:12]}"

def validate_mobile_money_number(number: str):
    """Basic validation for Cameroon mobile money numbers (MTN/Orange)."""
    return number.isdigit() and (number.startswith("67") or number.startswith("69")) and len(number) == 9