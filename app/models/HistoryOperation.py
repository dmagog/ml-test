import numpy as np
import pandas as pd
import datetime

from sqlmodel import SQLModel, Field 
from typing import Optional, List


class HistoryOperation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime.datetime = Field(default=datetime.datetime.now()) 
    user_id: int
    operation: str
    generation: str
    success: bool
