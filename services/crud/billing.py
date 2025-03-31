from sqlmodel import SQLModel, Field, select
from typing import Optional, List

from models.billing import *


# Операция пополнения балланса    
def update_BillOperationsList(new_operation: BillOperation, 
                              session) -> bool:
    session.add(new_operation) # создали новую запись в истории операций
    session.commit() 
    session.refresh(new_operation)
    #print(f"Пополнение баланса на {new_operation.payment} ед. для User_id:{new_operation.User_id} прошлошло успешно.") 

    return True


#Пополнение баланса
def update_Bill_refund(id: int, payment: float, session) -> bool:
    upd_Bill = session.get(Bill, id) 

    NewOperation = BillOperation(User_id = id, Val = payment, Success = False,
                                Operation = 'Пополнение баланса')
    if upd_Bill:
        upd_Bill.balance += payment
        NewOperation.Success = True

        session.add(upd_Bill) 
        session.commit() 
        session.refresh(upd_Bill)

    update_BillOperationsList(NewOperation, session)    
    return NewOperation.Success


def update_Bill_refillLimits(id: int, Num: float, session) -> bool:
    upd_Bill = session.get(Bill, id) 

    NewOperation = BillOperation(User_id = id, Val = Num, Success = False,
                                Operation = 'Пополнение суточного лимита бесплатных операций')
    if upd_Bill:
        if Num == 0:
             upd_Bill.FreeLimitToday = upd_Bill.FreeLimitPerDay    
        else:
            upd_Bill.FreeLimitToday += Num

        NewOperation.Success = True

        session.add(upd_Bill) 
        session.commit() 
        session.refresh(upd_Bill)

    update_BillOperationsList(NewOperation, session)    
    return NewOperation.Success


#Списание средств с баланса
def update_Bill_payment(id: int, payment: float, session) -> bool:
    upd_Bill = session.get(Bill, id) 

    NewOperation = BillOperation(User_id = id, Val = payment, Success = False,
                                Operation = 'Списание с баланса')
    if upd_Bill:
        if upd_Bill.balance - payment >= 0:
            upd_Bill.balance -= payment
            NewOperation.Success = True

            session.add(upd_Bill) 
            session.commit() 
            session.refresh(upd_Bill)

    update_BillOperationsList(NewOperation, session)    
    return NewOperation.Success


# Списание с копилки дневных лимитов
def update_Bill_decLimits(id: int, Num: float, session) -> bool:
    upd_Bill = session.get(Bill, id) 

    NewOperation = BillOperation(User_id = id, Val = Num, Success = False,
                                Operation = 'Списание бесплатных операций')
    if upd_Bill:
        if upd_Bill.FreeLimitToday - Num >= 0:
            upd_Bill.FreeLimitToday -= Num 

            NewOperation.Success = True

            session.add(upd_Bill) 
            session.commit() 
            session.refresh(upd_Bill)

    update_BillOperationsList(NewOperation, session)    
    return NewOperation.Success



#Счет пользователя по id клиента
def get_Bill(id: int, session) -> Bill:
    return session.get(Bill, id) 


# Получение истории операций по id пользователя
def get_Bill_OperationsList(id: int, session) -> BillOperation:
    return session.query(BillOperation).filter(BillOperation.User_id == id).all()

def get_Bill_OperationsList_2(id: int, session):
    statement = select(BillOperation).where(BillOperation.User_id == id)
    results = session.exec(statement)

    return results


#Списание средств с баланса
def pay(id: int, payment: float, session) -> bool:
    upd_Bill = session.get(Bill, id) 

    NewOperation = BillOperation(User_id = id, Val = payment, Success = False,
                                Operation = 'Платежная операция')
    
    # Если пользователь не исчерпал бесплатные операции на день - он ничего не платит
    # Если исчерпал - платит
    if upd_Bill:
        if update_Bill_decLimits(id, payment, session):
            NewOperation.Success = True
            NewOperation.Operation = 'Списание в счёт суточного лимита'
        elif update_Bill_payment(id, payment, session):
            NewOperation.Success = True
            NewOperation.Operation = 'Списание с баланса счета'
        else:
            NewOperation.Operation = 'Недостаточно средеств на счете' 

    update_BillOperationsList(NewOperation, session)    
    return NewOperation.Success
