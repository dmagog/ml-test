from models.user import User, userRole
from models.billing import *
from models.HistoryOperation import HistoryOperation
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import func

def create_user(new_user: User, 
                new_bill: Bill,
                session) -> None:
    session.add(new_user) # создали нового пользователя
    session.add(new_bill) # создали для него новый счет
    session.commit() 
    session.refresh(new_user)
    session.refresh(new_bill)


def get_all_users(session) -> List[User]:
    return session.query(User).all()


def get_user_by_id(id:int, session) -> Optional[User]:
    users = session.get(User, id) 
    if users:
        return users 
    return None


def get_user_by_email(email:str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user 
    return None



def delete_user(user_id: int, session: Session) -> bool:
    """
    Удалить пользователя по ID.
    
    Аргументы:
        user_id: ID пользователя для удаления
        session: Сессия базы данных
    
    Возвращает:
        bool: True если удален, False если не найден
    """
    try:
        user = get_user_by_id(user_id, session)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise



def get_users_with_bills(session):
    # Выполним SQL запрос с объединением таблиц
    result = session.query(User, Bill).join(Bill, User.id == Bill.id).all()

    users_with_bills = []
    for user, bill in result:
        # Преобразуем данные в удобный формат
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "role": user.role,
            "regDate": user.regDate,
            "balance": bill.balance,
            "freeLimit_today": bill.freeLimit_today,
            "freeLimit_perDay": bill.freeLimit_perDay
        }
        users_with_bills.append(user_data)
    
    return users_with_bills


def get_users_with_bills_and_history(session):
    # Объединяем пользователей со счетами и считаем количество операций, сортируя по id
    result = (
        session.query(
            User,
            Bill,
            func.count(HistoryOperation.id).label("operation_count")
        )
        .join(Bill, User.id == Bill.id)
        .outerjoin(HistoryOperation, User.id == HistoryOperation.user_id)
        .group_by(User.id, Bill.id)
        .order_by(User.id)  # <-- сортировка по id
        .all()
    )

    users_data = []
    for user, bill, operation_count in result:
        user_info = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "role": user.role,
            "regDate": user.regDate,
            "balance": bill.balance,
            "freeLimit_today": bill.freeLimit_today,
            "freeLimit_perDay": bill.freeLimit_perDay,
            "operations_count": operation_count
        }
        users_data.append(user_info)

    return users_data

def promote_user_role(user: User, session) -> bool:
    """
    Повышает роль пользователя на один уровень,
    но не позволяет установить роль superAdmin.

    Возвращает True, если повышение прошло успешно,
    и False, если повышение невозможно.
    """
    # if user.role == userRole.superAdmin:
    #     return False  # Повышать superAdmin нельзя

    # if user.role > userRole.megaUser:
    #     return False  # gigaUser — максимальный разрешённый уровень

    if user.role == 0: user.role = userRole(userRole.simpleUser)
    else: user.role = userRole(userRole.superAdmin)

    session.commit() 
    session.refresh(user)
    return True