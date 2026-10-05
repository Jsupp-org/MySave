from dataclasses import dataclass

TRANSACTION_TYPES = ("deposit", "withdraw")

@dataclass
class SavingsModel:
    folder_id: int
    transaction_type: str
    amount: float
    note: str | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        if self.transaction_type not in TRANSACTION_TYPES:
            raise ValueError("Transaction type must be 'deposit' or 'withdraw'.")
        if self.amount <= 0:
            raise ValueError("Please enter a positive amount.")