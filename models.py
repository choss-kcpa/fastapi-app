# models.py
import database  # 상대 경로 대신 절대 경로로 수정

# Pydantic 모델 정의
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float = None