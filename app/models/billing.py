import numpy as np
import pandas as pd
import datetime

from sqlmodel import SQLModel, Field 
from typing import Optional, List


class Bill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    balance: float # Текущий балланс
    freeLimit_today: float # сколько обесплатных операций осталось на сегодня
    freeLimit_perDay: float # сколько обесплатных операций в день доступно в принципе


class BillOperation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime.datetime = Field(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # Название операции
    user_id: int # идентификатор клиента, который совершил операцию
    operation: str # Название операции
    val: float # Значение операции
    success: bool # Успешность операции