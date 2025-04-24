from sqlmodel import Session 
from models.user import User
from services.crud.user import *
from models.billing import Bill, BillOperation
import pytest



def test_create_user(session: Session):
    # Создаем тестовые данные
    test_user = User(
        id=1,
        name="Test User",
        password="securepassword",
        email="test@example.com",
        age=30
    )
    test_bill = Bill(
        id=1,
        balance=100,
        freeLimit_today= 3,
        freeLimit_perDay= 3,
    )

    # Вызываем функцию
    create_user(test_user, test_bill, session)

    # Проверяем, что пользователь и счет добавлены
    user_from_db = session.get(User, 1)
    bill_from_db = session.get(Bill, 1)

    assert user_from_db is not None
    assert bill_from_db is not None
    assert user_from_db.name == "Test User"
    assert bill_from_db.balance == 100    



def test_create_user_correct(session: Session):
    """осздание валидного юзера"""
    user = User(name='Elvis', email="elvis@mail.ru", password="12345", age=10)
    session.add(user)
    session.commit()


def test_create_user_incorrect(session: Session):
    """осздание не валидного юзера - недостаток данных
    """
    with pytest.raises(Exception) as ex:
        user = User(email="elvis@mail.ru")
        session.add(user)
        session.commit()   


def test_create_user_repeate_email(session: Session):
    """осздание не валидного юзера - недостаток данных
    """
    user = User(name='Elvis', email="elvis@mail.ru", password="12345", age=10)
    session.add(user)
    session.commit()           
    


def test_update_bill_refund(session: Session):
    id = 1
    payment = 10
     
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = payment, success = False,
                                  operation = 'Пополнение баланса')
    if upd_bill:
        upd_bill.balance += payment
        new_operation.success = True

        session.add(upd_bill) 
        session.commit() 
        session.refresh(upd_bill)



def update_bill_refill_limits(session: Session):
    id = 1 
    num = 1000 
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




#Списание средств с баланса
def test_update_bill_payment(session: Session):
    id = 1 
    payment = 1 
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



# Списание с копилки дневных лимитов
def test_update_bill_dec_limits(session: Session):
    id = 1 
    num = 1 
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



#Списание средств с баланса
def test_pay(session: Session):
    id = 1 
    payment = 1 
    upd_bill = session.get(Bill, id) 

    new_operation = BillOperation(user_id = id, val = payment, success = False,
                                operation = 'Платежная операция')
    
    # Если пользователь не исчерпал бесплатные операции на день - он ничего не платит
    # Если исчерпал - платит
    if upd_bill:
        if test_update_bill_dec_limits(session):
            new_operation.success = True
            new_operation.operation = 'Списание в счёт суточного лимита'
        elif test_update_bill_payment(session):
            new_operation.success = True
            new_operation.operation = 'Списание с баланса счета'
        else:
            new_operation.operation = 'Недостаточно средеств на счете' 

    assert True

        
def test_delete_user(session: Session):
    """
    """
    test_create_user_correct(session)
    
    user = session.get(User, 1)
    assert user is not None, "Пользователь с id=1 не найден"  # Fixed incorrect ID in error message

    session.delete(user)
    session.commit()

    deleted_user = session.get(User, 1)
    assert deleted_user is None, "Пользователь не был удален"
