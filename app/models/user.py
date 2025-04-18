from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, List, TYPE_CHECKING
import re

import enum
import numpy as np
import pandas as pd
import datetime

from models.models import *
from models.HistoryOperation import HistoryOperation

if TYPE_CHECKING:
    from models.mltask import MLTask

class userRole(enum.IntEnum):
    superAdmin = 0
    simpleUser = 1
    megaUser = 2
    gigaUser = 3


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    password: str = Field(default='12345')
    email: str 
    age: int
    role: userRole = Field(default=1)
    regDate: datetime.datetime = Field(default=datetime.datetime.now())

    ml_tasks: List["MLTask"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __str__(self) -> str:
        """Строковое представление пользователя"""
        return f"Id: {self.id}. Email: {self.email}"

    def validate_email(self) -> bool:
        """
        Проверка формата электронной почты.
        
        Возвращает:
            bool: True если формат верный
        
        Вызывает:
            ValueError: Если формат электронной почты неверный
        """
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(self.email):
            raise ValueError("Неверный формат электронной почты")
        return True
    