from models.models import *
from models.HistoryOperation import *
from services.crud.billing import *
from services.crud.historyOperation import *


def create_model(new_model: MLmodel, 
                session) -> None:
    session.add(new_model) # создали новую модель в базе
    session.commit()
    session.refresh(new_model)



def useModel(model_id, user_id, session):
    model = session.get(MLmodel, model_id) 
    
    NewOperation = HistoryOperation(date = datetime.datetime.now(), user_id = user_id, success = False,
                                    operation = 'Запуск модели')
    if model:
        print('Стоимость модели = ', model.price)
        if pay(user_id, model.price, session):
            # Если платеж прошел, запускаем модель

            # 
            NewOperation.success = True

    print('Обновляем историю платежей')
    update_HistoryOperationsList(NewOperation, session)
    return NewOperation.success



#     def useModel(self, payment, model: MLmodel):
#         #Процедура запуска модели, с проверкой возможности запуска, сохранением параметров и списания баланса
#         ResultOperation = False # все плохо, если ничто это го не изменит

#         if self.billing.pay(payment):
#             # Если платеж прошел или мы можем провести операцию бесплатно в рамках лимита
#             model.run()
#             self.history.update(Date = datetime.datetime.now(),
#                                 Operation = 'Запуск модели',
#                                 Success = model.StatusOperation)

#             if not model.StatusOperation:
#                 # Если запуск модели был неудачный, нужно вернуть оплату 
#                 # Если операция шла за счет бесплатных, то вернем клиенту это деньгами (надеюсь, нас не обонкротят :О))
#                 self.billing.refund(payment)
#             else:
#                 ResultOperation = True

#         return ResultOperation    