from dataclasses import dataclass


@dataclass
class Employee:
    uid: int
    start_work_from: float
    salary: int
    name: str
    boss: int
    position_key: int

