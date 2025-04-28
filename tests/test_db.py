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
    user = User(id=5, name='Elvis', email="elvis@mail.ru", password="12345", age=45)
    session.add(user)
    session.commit()

    # Проверяем, что пользователь и счет добавлены
    user_from_db = session.get(User, 5)

    assert user_from_db is not None
    assert user_from_db == User(id=5, name='Elvis', email="elvis@mail.ru", password="12345", age=45)


def test_create_user_incorrect(session: Session):
    """осздание не валидного юзера - недостаток данных
    """
    with pytest.raises(Exception) as ex:
        user = User(email="elvis@mail.ru")
        session.add(user)
        session.commit()   

       
    


def test_update_bill_refund(session: Session):
    id = 1
    payment = 10
     
    # Попробуем найти счет
    upd_bill = session.get(Bill, id)

    # Если его нет — создадим тестовый счет
    if upd_bill is None:
        upd_bill = Bill(id=id, balance=0)  # начальный баланс = 0
        session.add(upd_bill)
        session.commit()


    balance_last = upd_bill.balance 

    new_operation = BillOperation(
        user_id=id, 
        val=payment, 
        success=False,
        operation='Пополнение баланса'
    )
    
    if upd_bill:
        upd_bill.balance += payment
        new_operation.success = True

        session.add(upd_bill)
        session.add(new_operation)  # не забудем сохранить саму операцию!
        session.commit()

        # Загружаем обновлённые данные из базы
        updated_bill = session.get(Bill, id)

        # Проверяем, что баланс увеличился на нужную сумму
        assert updated_bill.balance == balance_last + payment, \
            f"Баланс должен был увеличиться на {payment}, но стал {updated_bill.balance}"

        # Проверяем, что операция записалась и была успешной
        saved_operation = session.query(BillOperation).filter_by(user_id=id).order_by(BillOperation.id.desc()).first()
        assert saved_operation is not None, "Операция пополнения должна быть сохранена"
        assert saved_operation.success is True, "Операция пополнения должна быть успешной"
        assert saved_operation.val == payment, "Сумма пополнения должна соответствовать переданной"


def update_bill_refill_limits(session: Session):
    id = 1
    payment = 1000
     
    # Попробуем найти счет
    upd_bill = session.get(Bill, id)

    # Если его нет — создадим тестовый счет
    if upd_bill is None:
        upd_bill = Bill(id=id, balance=0)  # начальный баланс = 0
        session.add(upd_bill)
        session.commit()


    balance_last = upd_bill.freeLimit_today 

    new_operation = BillOperation(
        user_id=id, 
        val=payment, 
        success=False,
        operation='Пополнение суточного лимита бесплатных операций'
    )
    
    if upd_bill:
        upd_bill.freeLimit_today += payment
        new_operation.success = True

        session.add(upd_bill)
        session.add(new_operation)  # не забудем сохранить саму операцию!
        session.commit()

        # Загружаем обновлённые данные из базы
        updated_bill = session.get(Bill, id)

        # Проверяем, что баланс увеличился на нужную сумму
        assert updated_bill.freeLimit_today == balance_last + payment, \
            f"Баланс должен был увеличиться на {payment}, но стал {updated_bill.freeLimit_today}"

        # Проверяем, что операция записалась и была успешной
        saved_operation = session.query(BillOperation).filter_by(user_id=id).order_by(BillOperation.id.desc()).first()
        assert saved_operation is not None, "Операция пополнения должна быть сохранена"
        assert saved_operation.success is True, "Операция пополнения должна быть успешной"
        assert saved_operation.val == payment, "Сумма пополнения должна соответствовать переданной"    



def test_update_bill_payment(session: Session):
    id = 1
    payment = 1

    # Попробуем найти счет
    upd_bill = session.get(Bill, id)

    # Если счета нет — создадим тестовый счет с достаточным балансом
    if upd_bill is None:
        upd_bill = Bill(id=id, balance=payment + 5)  # чтобы хватило на списание
        session.add(upd_bill)
        session.commit()

    balance_last = upd_bill.balance

    new_operation = BillOperation(
        user_id=id,
        val=payment,
        success=False,
        operation='Списание с баланса'
    )

    if upd_bill.balance - payment >= 0:
        upd_bill.balance -= payment
        new_operation.success = True

        session.add(upd_bill)
        session.add(new_operation)
        session.commit()
        session.refresh(upd_bill)

        # Проверка: баланс уменьшился на сумму списания
        assert upd_bill.balance == balance_last - payment, \
            f"Баланс должен был уменьшиться на {payment}, но стал {upd_bill.balance}"

        # Проверка: операция списания успешно сохранилась
        saved_operation = session.query(BillOperation).filter_by(user_id=id).order_by(BillOperation.id.desc()).first()
        assert saved_operation is not None, "Операция списания должна быть сохранена"
        assert saved_operation.success is True, "Операция списания должна быть успешной"
        assert saved_operation.val == payment, "Сумма списания должна соответствовать переданной"
    else:
        pytest.fail("Недостаточно средств для списания")



def test_update_bill_dec_limits(session: Session):
    id = 1
    num = 1  # сколько хотим списать

    # Попробуем найти счет
    upd_bill = session.get(Bill, id)

    # Если счета нет — создаём тестовый с запасом лимита
    if upd_bill is None:
        upd_bill = Bill(id=id, balance=0, freeLimit_today=num + 5)  # чтобы хватило бесплатных лимитов
        session.add(upd_bill)
        session.commit()

    free_limit_last = upd_bill.freeLimit_today

    new_operation = BillOperation(
        user_id=id,
        val=num,
        success=False,
        operation='Списание бесплатных операций'
    )

    if upd_bill.freeLimit_today - num >= 0:
        upd_bill.freeLimit_today -= num
        new_operation.success = True

        session.add(upd_bill)
        session.add(new_operation)
        session.commit()
        session.refresh(upd_bill)

        # Проверка: лимит уменьшился на списанное количество
        assert upd_bill.freeLimit_today == free_limit_last - num, \
            f"Лимит бесплатных операций должен был уменьшиться на {num}, но стал {upd_bill.freeLimit_today}"

        # Проверка: операция успешно сохранилась
        saved_operation = session.query(BillOperation).filter_by(user_id=id).order_by(BillOperation.id.desc()).first()
        assert saved_operation is not None, "Операция списания бесплатных операций должна быть сохранена"
        assert saved_operation.success is True, "Операция списания бесплатных операций должна быть успешной"
        assert saved_operation.val == num, "Количество списаний должно соответствовать переданному"
    else:
        pytest.fail("Недостаточно бесплатных операций для списания")


        
def test_delete_user(session: Session):
    """
    """
    #test_create_user_correct(session)
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

    session.add(test_user) # создали нового пользователя
    session.add(test_bill) # создали для него новый счет
    session.commit() 
    session.refresh(test_user)
    session.refresh(test_bill)

    
    user = session.get(User, 1)
    assert user is not None, "Пользователь с id=1 не найден"  # Fixed incorrect ID in error message

    session.delete(user)
    session.commit()

    deleted_user = session.get(User, 1)
    assert deleted_user is None, "Пользователь не был удален"
