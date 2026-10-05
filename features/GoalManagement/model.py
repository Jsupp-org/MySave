from dataclasses import dataclass

@dataclass
class GoalModel:
    folder_id: int
    goal_amount: float

    def __post_init__(self) -> None:
        if self.goal_amount <= 0:
            raise ValueError("Please enter a positive amount.")