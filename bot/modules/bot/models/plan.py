from dataclasses import dataclass
from typing import Any


@dataclass
class Plan():
    name : str
    days : int 
    price: int
    
    @classmethod
    def from_dict(cls,data: dict[str,Any]) -> "Plan":
        return cls(
            name    = data["name"],
            price   = data["price"],
            days    = data["days"]
        )
