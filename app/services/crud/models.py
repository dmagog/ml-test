from models.models import *
from models.HistoryOperation import *
from services.crud.billing import *
from services.crud.historyOperation import *
from fastapi import APIRouter, HTTPException, Depends, Form
from typing import Dict, List
import logging
from models.mltask import MLTask, TaskStatus, MLTaskCreate
from services.logging.logging import get_logger
from services.crud.mltask import MLTaskService
from sqlmodel import Session
from services.rm.rpc import rpc_client

def create_model(new_model: MLmodel, 
                session) -> None:
    session.add(new_model) # создали новую модель в базе
    session.commit()
    session.refresh(new_model)


logging.getLogger('pika').setLevel(logging.INFO)
logger = get_logger(logger_name=__name__)
    

def use_model(model_id: int, user_id: int, session):
    model = session.get(MLmodel, model_id) 
    
    new_operation = HistoryOperation(date = datetime.datetime.now(), user_id = user_id, success = False,
                                    operation = f'Запуск модели {model_id}')
    if model:
        print('Стоимость модели = ', model.price)
        if pay(user_id, model.price, session):
            # Если платеж прошел, запускаем модель
            if model_id == 1: text_messsage = 'про Чапаева'
            if model_id == 2: text_messsage = 'про Штирлица'
            if model_id == 3: text_messsage = 'про Гарри Поттера'
            new_operation.operation = f'Анекдот {text_messsage}'
            #send_task_rpc_button(user_id, text_messsage, Depends(get_mltask_service))
            # 
            new_operation.success = True

    update_history_operations_list(new_operation, session)
    return new_operation.success


# def use_model(model_id, user_id, session):
#     model = session.get(MLmodel, model_id) 
    
#     new_operation = HistoryOperation(date = datetime.datetime.now(), user_id = user_id, success = False,
#                                     operation = f'Запуск модели {model_id}')
#     if model:
#         print('Стоимость модели = ', model.price)
#         if pay(user_id, model.price, session):
#             # Если платеж прошел, запускаем модель
                
#             # 
#             new_operation.success = True

#     update_history_operations_list(new_operation, session)
#     return new_operation.success


#     def use_model(self, payment, model: MLmodel):
#         #Процедура запуска модели, с проверкой возможности запуска, сохранением параметров и списания баланса
#         ResultOperation = False # все плохо, если ничто это го не изменит

#         if self.billing.pay(payment):
#             # Если платеж прошел или мы можем провести операцию бесплатно в рамках лимита
#             model.run()
#             self.history.update(Date = datetime.datetime.now(),
#                                 operation = 'Запуск модели',
#                                 success = model.StatusOperation)

#             if not model.StatusOperation:
#                 # Если запуск модели был неудачный, нужно вернуть оплату 
#                 # Если операция шла за счет бесплатных, то вернем клиенту это деньгами (надеюсь, нас не обонкротят :О))
#                 self.billing.refund(payment)
#             else:
#                 ResultOperation = True

#         return ResultOperation    