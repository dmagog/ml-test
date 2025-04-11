from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.models import *
from services.crud import models as ModelService
from typing import List

models_route = APIRouter(tags=['Models'])


@models_route.post("/{model_id}/{user_id}")
async def use_model(model_id, user_id, session=Depends(get_session)) :
    new_use = ModelService.use_model(model_id, user_id, session)
    if new_use is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot use model {model_id} for supplied user {user_id}")

    return {"message": f"Useage {model_id} for user {user_id} successfully!"}

