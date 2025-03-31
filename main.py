from models.user import *
from models.models import *
from models.billing import *
import random

from database.config import get_settings
from database.database import get_session, init_db, engine
from services.crud.user import *
from services.crud.billing import *
from services.crud.models import *
from sqlmodel import Session
import datetime



if __name__ == "__main__":

    settings = get_settings()
    # print('gfo gso = ', settings.DB_HOST)
    # print('gfo gso = =', settings.DB_NAME)

    init_db(demostart = True)
    print('Init db has been success')

    # test_user = User(name = 'Harry', email='test@mail.ru', age=10, regDate = datetime.datetime.now())
    # test_user_2 = User(name = 'Ron', email='test@mail.ru', age=10, regDate = datetime.datetime.now())
    # test_user_3 = User(name = 'Hermione', email='test@mail.ru', age=10, regDate = datetime.datetime.now())

    # with Session(engine) as session:
    #     create_user(test_user, 
    #                 Bill(balance=10, FreeLimitPerDay=3, FreeLimitToday=3), session)
    #     create_user(test_user_2, 
    #                 Bill(balance=10, FreeLimitPerDay=3, FreeLimitToday=3), session)
    #     create_user(test_user_3, 
    #                 Bill(balance=10, FreeLimitPerDay=3, FreeLimitToday=3), session)
    #     users = get_all_users(session)

    # for user in users:
    #     print(f'id: {user.id} - {user.email}')


    update_BillOperationsList(BillOperation(Date = datetime.datetime.now(),
                                            User_id=1,
                                            Operation='Что -то тестовое с чем то странным-1',
                                            Val= -2,
                                            Success=True), Session(engine))
    update_BillOperationsList(BillOperation(Date = datetime.datetime.now(),
                                            User_id=2,
                                            Operation='Что -то тестовое с чем то странным-2',
                                            Val= -1,
                                            Success=True), Session(engine))
    update_BillOperationsList(BillOperation(Date = datetime.datetime.now(),
                                            User_id=3,
                                            Operation='Что -то тестовое с чем то странным-3',
                                            Val= -10,
                                            Success=True), Session(engine))
    

    

    for _ in range(1, 10):
        Model_id = random.randint(1,2)
        User_id = random.randint(1,4)
        useModel(Model_id, User_id, Session(engine))

    # update_Bill_refund(1, payment = 1, session = Session(engine))
    # update_Bill_refillLimits(10, Num = 1, session = Session(engine))
    # update_Bill_refillLimits(1, Num = 0, session = Session(engine))

    # pay(1, 2, session = Session(engine))
    # pay(1, 1, session = Session(engine))
    # pay(1, 1, session = Session(engine))
    # pay(1, 2, session = Session(engine))
    # pay(1, 1, session = Session(engine))

    # print('\n\nВывод истории операций пользоывателя')
    # print(get_Bill_OperationsList(1, session = Session(engine)))

    # print('\n\n2222 Вывод истории операций пользоывателя  222')
    # print(get_Bill_OperationsList_2(1, session = Session(engine)))

    # Инициируем модели
    #CurrModel_1 = UsableModel('', 'Убиватор-3000', '1.01', 'Офигенская модель, прям всем советую только ее',
    #                        price = 1)

    #CurrModel_2 = UsableModel('', 'УльтраУбиватор-9000', '3.33', 'Еще более крутая и дорогая модель.',
    #                        price = 2)
    
    # Для демонстрации сделаем выбор модели случайным образом
    #if bool(random.randint(0, 1)): CurrModel = CurrModel_1
    #else: CurrModel = CurrModel_2


    # Создание пользователя
    # CurrentUser = User(name = 'dmagog',
    #                 email = 'georgy-mamarin@mail.ru',
    #                 role = 1,
    #                 startbalance = 5,
    #                 FreeLimitPerDay = 3)

    # print(CurrentUser)


    
    # for _ in range(0,5):
    #     #Пользователь вызывает модель
    #     CurrentUser.useModel(model = CurrModel, 
    #                         payment = CurrModel.price)

    
    # print()
    # print('Балланс = ', CurrentUser.billing.get_balance())
    # print('Бесплатных операций осталось = ', CurrentUser.billing.get_limits())
    # print('Последняя операция = ', CurrentUser.history.get_lastOperationDate())
    # print('Всего операций = ', CurrentUser.history.get_OperationAll())
    # print('Операций cегодня = ', CurrentUser.history.get_OperationToday())

    # print()
    # print(CurrentUser.history.get())

    # print()
    # print(CurrentUser.billing.get_operations())