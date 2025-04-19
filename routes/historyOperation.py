from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.HistoryOperation import *
from services.crud import historyOperation as HistoryService
from typing import List

history_operations_route = APIRouter(tags=['History'])


@history_operations_route.get("/{id}", response_model=List[HistoryOperation])
async def get_history_operations_list(id: int, session=Depends(get_session)) -> List[HistoryOperation]:
    hystory_operations = HistoryService.get_history_operations_list(id, session)
    if hystory_operations:
        return hystory_operations
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History operations for supplied ID does not exist")