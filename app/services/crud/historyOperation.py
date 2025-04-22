from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict
from models.HistoryOperation import *
from models.user import User
from sqlalchemy import func, case


# Операция пополнения балланса    
def update_history_operations_list(new_operation: HistoryOperation, session) -> bool:
    new_operation.date = new_operation.date.strftime("%Y-%m-%d %H:%M:%S")
    session.add(new_operation)  # создали новую запись в истории операций
    session.commit() 
    session.refresh(new_operation)

    return True

# Получение истории операций по id пользователя
def get_history_operations_list(id: int, session) -> List[HistoryOperation]:
    return session.query(HistoryOperation).filter(HistoryOperation.user_id == id).all()


def get_last_operation_by_userid(user_id: int, session) -> Optional[HistoryOperation]:
    return (
        session.query(HistoryOperation)
        .filter(HistoryOperation.user_id == user_id)
        .order_by(HistoryOperation.date.desc())
        .first()
    )


def get_successful_operations_summary(session) -> List[Dict]:
    # Получаем всех пользователей с подсчетом только успешных операций
    results = (
        session.query(
            User.id,
            User.name,
            User.age,
            func.coalesce(
                func.sum(
                    case((HistoryOperation.success == True, 1), else_=0)
                ),
                0
            ).label("successful_operations"),
            func.rank().over(
                order_by=func.coalesce(
                    func.sum(
                        case((HistoryOperation.success == True, 1), else_=0)
                    ),
                    0
                ).desc()
            ).label("ranking")  # Добавляем рейтинг
        )
        .outerjoin(HistoryOperation, HistoryOperation.user_id == User.id)
        .group_by(User.id)
        .order_by(func.coalesce(
                    func.sum(
                        case((HistoryOperation.success == True, 1), else_=0)
                    ),
                    0
                ).desc())  # Сортировка по убыванию успешных операций
        .all()
    )

    # Формируем итоговый список
    summary = []
    for user_id, name, age, successful_operations, ranking in results:
        summary.append({
            "user_id": user_id,
            "name": name,
            "age": age,
            "successful_operations": successful_operations,
            "ranking": ranking
        })
    
    return summary