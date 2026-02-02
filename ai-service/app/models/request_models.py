from pydantic import BaseModel
from typing import List, Optional

class UserMetadata(BaseModel):
    current_balance: float
    credit_card_debt: float  # Yeni
    salary: float           # Yeni
    salary_day: int          # Yeni

class Transaction(BaseModel):
    id: str
    date: str
    amount: float
    description: str
    mcc_code: str
    category: str

class AnalysisRequest(BaseModel):
    user_metadata: UserMetadata
    transactions: List[Transaction]