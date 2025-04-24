from sqlmodel import Session 
from models.user import User
from services.crud.user import *
from services.crud.historyOperation import *
from models.billing import Bill, BillOperation
import datetime
import pytest


def test_update_history_success(session):
    new_op = HistoryOperation(
        date=datetime.datetime.now(),
        user_id=1,
        operation="Пополнение счёта",
        generation="-",
        success=True
    )

    success, error = update_history_operations_list(new_op, session)
    assert success is True
    assert error is None

    op = session.exec(select(HistoryOperation).where(HistoryOperation.user_id == 1)).first()
    assert op is not None   



def test_update_history_invalid_date_type(session):
    new_op = HistoryOperation(
        date="2025-04-24",  # не datetime
        user_id=3,
        operation="Генерация",
        generation="анекдот",
        success=True
    )

    success, error = update_history_operations_list(new_op, session)
    assert success is False
    assert "date" in error or "strptime" in error


def test_get_history_operations_for_existing_user(session):
    # Подготовка: создадим 2 операции
    session.add_all([
        HistoryOperation(user_id=10, operation="Пополнение", generation="-", success=True),
        HistoryOperation(user_id=10, operation="Генерация", generation="анекдот", success=True)
    ])
    session.commit()

    operations = get_history_operations_list(10, session)
    assert isinstance(operations, list)
    assert len(operations) == 2
    assert operations[0].user_id == 10



def test_get_history_operations_for_user_with_no_ops(session):
    operations = get_history_operations_list(9999, session)
    assert isinstance(operations, list)
    assert len(operations) == 0


def test_get_history_operations_invalid_user_id(session):
    operations = get_history_operations_list(-1, session)
    assert isinstance(operations, list)
    assert len(operations) == 0  # Или можно было бы вернуть ошибку, если добавить проверку


def test_get_history_operations_fields(session):
    session.add(
        HistoryOperation(user_id=20, operation="Тест", generation="—", success=True)
    )
    session.commit()

    operations = get_history_operations_list(20, session)
    op = operations[0]

    assert hasattr(op, "id")
    assert hasattr(op, "user_id")
    assert hasattr(op, "operation")
    assert hasattr(op, "generation")
    assert hasattr(op, "success")
    assert hasattr(op, "date")
