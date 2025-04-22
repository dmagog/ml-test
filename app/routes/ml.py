import logging
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends, Form
from sqlmodel import Session
from database.database import get_session
from models.mltask import MLTask, TaskStatus, MLTaskCreate
from services.rm.rpc import rpc_client
from services.logging.logging import get_logger
from models.HistoryOperation import HistoryOperation
from models.models import MLmodel
from services.crud.mltask import MLTaskService
from services.crud.billing import pay, update_bill_payment
from services.crud.historyOperation import update_history_operations_list
from fastapi.responses import RedirectResponse
import datetime
from database.database import get_session

logging.getLogger('pika').setLevel(logging.INFO)

logger = get_logger(logger_name=__name__)

ml_route = APIRouter()

def get_mltask_service(session: Session = Depends(get_session)) -> MLTaskService:
    return MLTaskService(session)



@ml_route.post("/send_task_rpc_button/{user_id}")
async def send_task_rpc_button(user_id: int, model_id: int = Form(...), mltask_service: MLTaskService = Depends(get_mltask_service), session: Session = Depends(get_session)) -> Dict[str, str]:
    model = session.get(MLmodel, model_id) 
    
    new_operation = HistoryOperation(date = datetime.datetime.now(), user_id = user_id, success = False,
                                    operation = f'Запуск модели {model_id}')

    if pay(user_id, model.price, session):

        try:
            if model_id == 1: message = 'про Чапаева'
            if model_id == 2: message = 'про Штирлица'
            if model_id == 3: message = 'про Гарри Поттера'
            new_operation.operation = f'Анекдот {message}'

            # Create task using service
            task_create = MLTaskCreate(
                question=message,
                user_id=user_id,
                status=TaskStatus.NEW
            )
            ml_task = mltask_service.create(task_create) 

            logger.info(f"Sending RPC request with message: {message}")
            result = rpc_client.call(text=message)
            logger.info(f"Received RPC response: {result}")

            # Update task with result using service
            mltask_service.set_result(ml_task.id, result)

            if result:
                new_operation.generation = result
                new_operation.success = True
            
            update_history_operations_list(new_operation, session)
            #return {"original": message, "processed": result}
            return RedirectResponse(url="/private/history/", status_code=303)
        except Exception as e:
            logger.error(f"Unexpected error in RPC call: {str(e)}")
            if ml_task:
                mltask_service.set_status(ml_task.id, TaskStatus.FAILED)
            # raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
            return RedirectResponse(url="/private/history/", status_code=500)
    else: 
        return RedirectResponse(url="/private/history/", status_code=303)

@ml_route.post("/send_task_rpc", response_model=Dict[str, str])
async def send_task_rpc(
    message: str,
    user_id: int,
    mltask_service: MLTaskService = Depends(get_mltask_service)
) -> Dict[str, str]:
    """
    Endpoint for sending ML task using RPC.

    Args:
        message (str): The message to be sent.
        user_id (int): ID of the user creating the task.

    Returns:
        Dict[str, str]: Response message with original and processed text.
    """
    
    try:
        # Create task using service
        task_create = MLTaskCreate(
            question=message,
            user_id=user_id,
            status=TaskStatus.NEW
        )
        ml_task = mltask_service.create(task_create) 

        logger.info(f"Sending RPC request with message: {message}")
        result = rpc_client.call(text=message)
        logger.info(f"Received RPC response: {result}")

        # Update task with result using service
        mltask_service.set_result(ml_task.id, result)
        
        return {"original": message, "processed": result}
    except Exception as e:
        logger.error(f"Unexpected error in RPC call: {str(e)}")
        if ml_task:
            mltask_service.set_status(ml_task.id, TaskStatus.FAILED)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



@ml_route.get("/tasks", response_model=List[MLTask])
async def get_all_tasks(
    mltask_service: MLTaskService = Depends(get_mltask_service)
):
    """Get all ML tasks."""
    return mltask_service.get_all()

@ml_route.get("/tasks/{task_id}", response_model=MLTask)
async def get_task_by_id(
    task_id: int,
    mltask_service: MLTaskService = Depends(get_mltask_service)
):
    """Get ML task by ID."""
    task = mltask_service.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@ml_route.get("{user_id}/tasks/", response_model=List[MLTask])
async def get_task_by_user(
    user_id: int,
    mltask_service: MLTaskService = Depends(get_mltask_service)
):
    """Get ML task by ID."""
    task = mltask_service.get_by_user_id(user_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Tasks for user whith id {user_id} not found")
    return task