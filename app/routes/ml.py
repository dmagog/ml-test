from typing import Dict
from fastapi import APIRouter, HTTPException
from services.rm.rm import send_task

ml_route = APIRouter()

@ml_route.post("/send_test", response_model=Dict[str, str],
               summary="Test ML endpoint",
               description="Send test ml request"
)
async def index(message:str) -> str:
    try:
        send_task(message)
        return {"message": f"Task sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@ml_route.post("/send_task/{model_id}/{user_id}", response_model=Dict[str, str],
               summary="ML endpoint",
               description="Send ml request"
)
async def index(model_id, user_id) -> str:
    try:
        message = f'{model_id}//{user_id}'
        send_task(message)
        return {"message": f"Task to use model {model_id} for user {user_id} sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)