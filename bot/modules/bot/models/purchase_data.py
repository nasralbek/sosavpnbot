from dataclasses import dataclass
from .import Plan

@dataclass
class PurchaseData(Plan):
    user_id : int   = 0
