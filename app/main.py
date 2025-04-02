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




    update_bill_operationsList(BillOperation(date = datetime.datetime.now(),
                                            user_id=1,
                                            operation='Что -то тестовое с чем то странным-1',
                                            val= -2,
                                            success=True), Session(engine))
    update_bill_operationsList(BillOperation(date = datetime.datetime.now(),
                                            user_id=2,
                                            operation='Что -то тестовое с чем то странным-2',
                                            val= -1,
                                            success=True), Session(engine))
    update_bill_operationsList(BillOperation(date = datetime.datetime.now(),
                                            user_id=3,
                                            operation='Что -то тестовое с чем то странным-3',
                                            val= -10,
                                            success=True), Session(engine))
    

    

    for _ in range(1, 10):
        model_id = random.randint(1,2)
        user_id = random.randint(1,4)
        use_model(model_id, user_id, Session(engine))


    print('\n\nВывод истории операций пользоывателя')
    print(get_bill_operationsList(1, session = Session(engine)))

    #print('\n\n2222 Вывод истории операций пользоывателя  222')
    #print(get_bill_operationsList_2(1, session = Session(engine)))

  


 