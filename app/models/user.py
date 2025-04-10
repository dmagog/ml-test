from sqlmodel import SQLModel, Field 
from typing import Optional, List

import enum
import numpy as np
import pandas as pd
import datetime

from models.models import *
from models.HistoryOperation import HistoryOperation


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

