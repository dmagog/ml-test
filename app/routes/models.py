from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.responses import RedirectResponse
from database.database import get_session
from models.models import *
from services.crud import models as ModelService
from typing import List
import random

models_route = APIRouter(tags=['Models'])


@models_route.post("/{user_id}")
async def use_model(user_id: int, model_id: int = Form(...), session=Depends(get_session)) :
    new_use = ModelService.use_model(model_id, user_id, session)
    if new_use is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot use model {model_id} for supplied user {user_id}")

    return RedirectResponse(url="/private/history", status_code=303) #{"message": f"Useage {model_id} for user {user_id} successfully!"}