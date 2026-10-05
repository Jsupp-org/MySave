from dataclasses import dataclass

@dataclass
class SavingsFolderModel:
    name: str
    goal_amount: float = 0.0
    current_amount: float = 0.0
    id: int | None = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Folder name is required.")
        if len(self.name) < 2:
            raise ValueError("Folder name must have at least 2 characters.")
        if self.goal_amount < 0:
            raise ValueError("Goal cannot be negative.")
        if self.current_amount < 0:
            raise ValueError("Balance cannot be negative.")