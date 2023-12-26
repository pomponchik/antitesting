from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class TestSpecification:
    name: str
    date_before_disabled: date
    disabled: bool = True

    def __post_init__(self) -> None:
        if datetime.now().date() > self.date_before_disabled:
            self.disabled = False
