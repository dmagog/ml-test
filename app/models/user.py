import enum
import numpy as np
import pandas as pd
import datetime

from models.models import UsableModel, MLmodel
from models.billing import Billing
from models.HistoryOperation import HistoryOperation


class UserRole(enum.IntEnum):
    superAdmin = 0
    simpleUser = 1
    megaUser = 2
    gigaUser = 3


class User:

    def __init__(self, name: str, email: str, role, startbalance: int, FreeLimitPerDay: int):
        self.name = name # имя пользователя
        self.email = email # электронный адрес для взаимодействия
        self.RegDate = datetime.datetime.now() # Дата-время регистрации
        self.role = UserRole(role) # Роль, по умолчанию "пользователь"
        
        self.billing = Billing(startbalance, FreeLimitPerDay) # Баланс пользователя в деньгах и свободных лимитах

        self.history = HistoryOperation() # история операций пользователя


    def useModel(self, payment, model: MLmodel):
        #Процедура запуска модели, с проверкой возможности запуска, сохранением параметров и списания баланса
        ResultOperation = False # все плохо, если ничто это го не изменит

        if self.billing.pay(payment):
            # Если платеж прошел или мы можем провести операцию бесплатно в рамках лимита
            model.run()
            self.history.update(Date = datetime.datetime.now(),
                                Operation = 'Запуск модели',
                                Success = model.StatusOperation)

            if not model.StatusOperation:
                # Если запуск модели был неудачный, нужно вернуть оплату 
                # Если операция шла за счет бесплатных, то вернем клиенту это деньгами (надеюсь, нас не обонкротят :О))
                self.billing.refund(payment)
            else:
                ResultOperation = True

        return ResultOperation





# Функция вывода профиля пользователя
def showUserDetails(CurrentUser):
    print('Имя пользователя = ', CurrentUser.name)
    print('Эл. почта = ', CurrentUser.email)
    print('Дата регистрации = ', CurrentUser.RegDate)
    print('Роль = ', CurrentUser.role)
    print('Бесплатных операций в день = ', CurrentUser.billing.get_limits())

    print()
    print('Балланс = ', CurrentUser.billing.get_balance())
    print('Бесплатных операций осталось = ', CurrentUser.billing.get_limits())
    print('Последняя операция = ', CurrentUser.history.get_lastOperationDate())
    print('Всего операций = ', CurrentUser.history.get_OperationAll())
    print('Операций cегодня = ', CurrentUser.history.get_OperationToday())


    print()
    print('Иницализация = ', CurrentUser.history.get_Initiation())