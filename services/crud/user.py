from models.user import User
from models.billing import *
from typing import List, Optional

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

