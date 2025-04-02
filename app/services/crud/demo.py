from sqlmodel import SQLModel, Field, select
from typing import Optional, List

from models.user import *
from services.crud.user import *
from services.crud.billing import *
from services.crud.models import *
import random

def create_demo_user(session):
    test_user = User(name = 'Harry', email='test@mail.ru', age=10, regDate = datetime.datetime.now(), role = 1)
    test_user_2 = User(name = 'Ron', email='test@mail.ru', age=10, regDate = datetime.datetime.now(), role = 1)
    test_user_3 = User(name = 'Hermione', email='test@mail.ru', age=10, regDate = datetime.datetime.now(), role = 1)
    test_user_4 = User(name = 'Dumbledor', email='test@mail.ru', age=100, regDate = datetime.datetime.now(), role = 0)

    create_user(test_user, 
                Bill(balance=10, freeLimit_perDay=3, freeLimit_today=3), session)
    create_user(test_user_2, 
                Bill(balance=10, freeLimit_perDay=3, freeLimit_today=3), session)
    create_user(test_user_3, 
                Bill(balance=10, freeLimit_perDay=3, freeLimit_today=3), session)
    create_user(test_user_4, 
                Bill(balance=20, freeLimit_perDay=5, freeLimit_today=5), session)


def create_demo_operations_list(session):
    for _ in range(0,10):
        user_id = random.randint(1,4)
        payment = random.randint(1,3)
        pay_or_refund = bool(random.random())
        if pay_or_refund: pay(user_id, payment, session)
        else: update_bill_refund(user_id, payment, session)



def create_demo_model(session):
    new_model_1 = MLmodel(model='',
                        name = 'Убиватор-3000', 
                        version = '1.01', 
                        description = 'Офигенская модель, прям всем советую только ее',
                        price = 1)

    new_model_2 = MLmodel(model='',
                        name = 'УльтраУбиватор-9000', 
                        version = '3.33', 
                        description = 'Еще более крутая и дорогая модель.',
                        price = 2)
    
    create_model(new_model_1, session)
    create_model(new_model_2, session)
