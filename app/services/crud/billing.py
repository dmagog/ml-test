from sqlmodel import SQLModel, Field, select
from typing import Optional, List

from models.billing import *


# Операция пополнения балланса    
def update_bill_operationsList(new_operation: BillOperation, 
                               session) -> bool:
    session.add(new_operation) # создали новую запись в истории операций
    session.commit() 
    session.refresh(new_operation)
    #print(f"Пополнение баланса на {new_operation.payment} ед. для user_id:{new_operation.user_id} прошлошло успешно.") 

    return True


#Пополнение баланса
def update_bill_refund(id: int, payment: float, session) -> bool:
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = payment, success = False,
                                  operation = 'Пополнение баланса')
    if upd_bill:
        upd_bill.balance += payment
        new_operation.success = True

        session.add(upd_bill) 
        session.commit() 
        session.refresh(upd_bill)

    update_bill_operationsList(new_operation, session)    
    return new_operation.success


def update_bill_refillLimits(id: int, num: float, session) -> bool:
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = num, success = False,
                                  operation = 'Пополнение суточного лимита бесплатных операций')
    if upd_bill:
        if num == 0:
             upd_bill.freeLimit_today = upd_bill.freeLimit_perDay    
        else:
            upd_bill.freeLimit_today += num

        new_operation.success = True

        session.add(upd_bill) 
        session.commit() 
        session.refresh(upd_bill)

    update_bill_operationsList(new_operation, session)    
    return new_operation.success


#Списание средств с баланса
def update_bill_payment(id: int, payment: float, session) -> bool:
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = payment, success = False,
                                  operation = 'Списание с баланса')
    if upd_bill:
        if upd_bill.balance - payment >= 0:
            upd_bill.balance -= payment
            new_operation.success = True

            session.add(upd_bill) 
            session.commit() 
            session.refresh(upd_bill)

    update_bill_operationsList(new_operation, session)    
    return new_operation.success


# Списание с копилки дневных лимитов
def update_Bill_decLimits(id: int, num: float, session) -> bool:
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = num, success = False,
                                  operation = 'Списание бесплатных операций')
    if upd_bill:
        if upd_bill.freeLimit_today - num >= 0:
            upd_bill.freeLimit_today -= num 

            new_operation.success = True

            session.add(upd_bill) 
            session.commit() 
            session.refresh(upd_bill)

    update_bill_operationsList(new_operation, session)    
    return new_operation.success



#Счет пользователя по id клиента
def get_bill(id: int, session) -> Bill:
    return session.get(Bill, id) 


# Получение истории операций по id пользователя
def get_bill_operationsList(id: int, session) -> BillOperation:
    return session.query(BillOperation).filter(BillOperation.user_id == id).all()

def get_bill_operationsList_2(id: int, session):
    statement = select(BillOperation).where(BillOperation.user_id == id)
    results = session.exec(statement)

    return results


#Списание средств с баланса
def pay(id: int, payment: float, session) -> bool:
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = payment, success = False,
                                operation = 'Платежная операция')
    
    # Если пользователь не исчерпал бесплатные операции на день - он ничего не платит
    # Если исчерпал - платит
    if upd_bill:
        if update_Bill_decLimits(id, payment, session):
            new_operation.success = True
            new_operation.operation = 'Списание в счёт суточного лимита'
        elif update_bill_payment(id, payment, session):
            new_operation.success = True
            new_operation.operation = 'Списание с баланса счета'
        else:
            new_operation.operation = 'Недостаточно средеств на счете' 

    update_bill_operationsList(new_operation, session)    
    return new_operation.success
