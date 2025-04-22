# Простой класс для хранения модели и ее обще описательных характеристик
import random
from sqlmodel import SQLModel, Field 
from typing import Optional, List


class MLmodel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    model: str
    name: str
    version: str 
    description: str
    price: float


