from sqlmodel import SQLModel, Field 
from typing import Optional, List
from models.HistoryOperation import *


# Операция пополнения балланса    
def update_history_operationsList(new_operation: HistoryOperation, session) -> bool:
    session.add(new_operation)  # создали новую запись в истории операций
    session.commit() 
    session.refresh(new_operation)

    return True