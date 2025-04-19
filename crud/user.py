from models.user import User
from models.billing import *
from typing import List, Optional
from sqlmodel import Session, select

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

