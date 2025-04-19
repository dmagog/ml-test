from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth.authenticate import authenticate_cookie, authenticate
from auth.hash_password import HashPassword
from database.config import get_settings
from database.database import get_session
from services.crud import user as UsersService
from services.crud import billing as BillService
from services.crud import historyOperation as HistoryService
import pandas as pd
from typing import Dict

settings = get_settings()
home_route = APIRouter()
hash_password = HashPassword()
templates = Jinja2Templates(directory="view")

@home_route.get("/", response_class=HTMLResponse)
async def index(request: Request, session=Depends(get_session)):
    """
    Главная страница приложения.
    
    Args:
        request (Request): Объект запроса FastAPI

    Returns:
        HTMLResponse: HTML страница с контекстом пользователя
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        user = await authenticate_cookie(token)
    else:
        user = None

    context = {
        "login": user,
        "request": request
    }

    if user:
        user_exist = UsersService.get_user_by_email(context['login'], session)
        if user_exist is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        
        context['user'] = user_exist


    return templates.TemplateResponse("index.html", context)


@home_route.get("/private", response_class=HTMLResponse)
async def index_private(request: Request, user:str=Depends(authenticate_cookie), session=Depends(get_session)):
    """
    Приватная страница, доступная только авторизованным пользователям через cookie.
    
    Args:
        request (Request): Объект запроса FastAPI
        user (str): Информация о пользователе из cookie-аутентификации

    Returns:
        HTMLResponse: Приватная HTML страница
    """
    context = {
        "login": user,
        "request": request
    }

    user_exist = UsersService.get_user_by_email(context['login'], session)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    context['user'] = user_exist


    bill_exist = BillService.get_bill(user_exist.id, session)
    if bill_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Bill does not exist")
    
    context['bill'] = bill_exist

    return templates.TemplateResponse("private.html", context)



@home_route.get("/private/billing", response_class=HTMLResponse)
async def index_private(request: Request, user:str=Depends(authenticate_cookie), session=Depends(get_session)):
    """
    Приватная страница, доступная только авторизованным пользователям через cookie.
    
    Args:
        request (Request): Объект запроса FastAPI
        user (str): Информация о пользователе из cookie-аутентификации

    Returns:
        HTMLResponse: Приватная HTML страница
    """
    context = {
        "login": user,
        "request": request
    }

    user_exist = UsersService.get_user_by_email(context['login'], session)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    context['user'] = user_exist


    bill_exist = BillService.get_bill(user_exist.id, session)
    if bill_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Bill does not exist")
    
    context['bill'] = bill_exist

    bill_operations_list_exist = BillService.get_bill_operations_list(user_exist.id, session)
    if bill_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User bill_operations_list does not exist")
    
    context['bill_operations_list_exist'] = pd.DataFrame(list(bill_operations_list_exist), columns=['id', 'user_id', 'val', 'date', 'operation', 'success'])
    #context['bill_operations_list_exist'] = list(bill_operations_list_exist)
    

    return templates.TemplateResponse("private_billing.html", context)



@home_route.get("/private/history", response_class=HTMLResponse)
async def index_private(request: Request, user:str=Depends(authenticate_cookie), session=Depends(get_session)):

    context = {
        "login": user,
        "request": request
    }

    user_exist = UsersService.get_user_by_email(context['login'], session)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    context['user'] = user_exist


    history_exist = HistoryService.get_history_operations_list(user_exist.id, session)
    if history_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User history operation list does not exist")
    
    
    context['history'] = list(history_exist)
    

    return templates.TemplateResponse("private_history.html", context)



@home_route.get(
    "/health",
    response_model=Dict[str, str],
    summary="Проверка работоспособности",
    description="Возвращает статус работоспособности сервиса"
)
async def health_check() -> Dict[str, str]:
    """
    Эндпоинт проверки работоспособности сервиса.

    Returns:
        Dict[str, str]: Сообщение о статусе работоспособности
    
    Raises:
        HTTPException: Если сервис недоступен
    """
    try:
        # Add actual health checks here
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail="Service unavailable"
        )

