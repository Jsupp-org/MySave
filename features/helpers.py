import math

def parse_amount(text: str) -> float:
    try: 
        amount = float(text.strip().replace(",", ""))
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")
    if not math.isfinite(amount):
        raise ValueError("Invalid input. Please enter a number.")
    return round(amount, 2)