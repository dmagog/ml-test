import numpy as np
import pandas as pd
import datetime

class PyamentsHistory:

    def __init__(self):
        self.__LastOperationDate = np.nan # Дата последней удачной операции
        self.__Operations = pd.DataFrame(columns=['Date', 'Operation', 'Val', 'Success']) # Список всех операций и дата свершения

    def get(self):
        return self.__Operations


    def update(self, Date, Operation: str, Val: float, Success: bool):
        LastPos = len(self.get())
        self.__Operations.loc[LastPos, 'Date'] = Date
        self.__Operations.loc[LastPos, 'Operation'] = Operation
        self.__Operations.loc[LastPos, 'Val'] = Val
        self.__Operations.loc[LastPos, 'Success'] = Success

        self.set_lastOperationDate()

    def get_Operations(self):
        return self.__Operations

    def get_lastOperationDate(self):
        return self.__LastOperationDate
    
    def set_lastOperationDate(self, OperationDate = datetime.datetime.now()):
        self.__LastOperationDate = OperationDate





class Billing:

    def __init__(self, startbalance: float, FreeLimitPerDay: int):
        self.__balance = startbalance # Стартовый балланс
        self.__FreeLimitToday = FreeLimitPerDay # сколько обесплатных операций осталось на сегодня
        self.__FreeLimitPerDay = FreeLimitPerDay # сколько обесплатных операций осталось на сегодня

        self.__Operations = PyamentsHistory() #история платежных операций



    # Операция пополнения балланса    
    def refund(self, payment: float):
        self.__balance += payment
        print(f"Пополнение баланса на {payment} ед. прошлошло успешно. Текущий балланс — {self.__balance} ед.") 

        self.__Operations.update(Date = datetime.datetime.now(), 
                              Operation = 'Пополнение баланса', 
                              Val = payment,
                              Success = True)          



    # Операция возобновления суточных лимитов
    def refillLimits(self, Num = None):
        # если Num == 0, значит возобновим лимит полностью
        # во всех остальных случаях делаем +Num
        if Num == None:
            self.__FreeLimitToday = self.__FreeLimitPerDay
        else:
            self.__FreeLimitToday += Num

            self.__Operations.update(Date = datetime.datetime.now(), 
                              Operation = 'Восполнение суточного лимита бесплатных операций', 
                              Val = Num,
                              Success = True)   
        
        print(f"Лимиты бесплатных вызовов в день обновлены. Сейчас доступно — {self.__FreeLimitToday}")



    # Операция получения балланса пользователя
    def get_balance(self):
        return self.__balance
    
    # Операция получения балланса пользователя
    def get_limits(self):
        return self.__FreeLimitToday
    
    # Операция получения истории операций билинга
    def get_operations(self):
        return self.__Operations.get_Operations()
    

    # списываем с дневного лимита 
    def set_decLimints(self, limitPayment = 1):
        if self.get_limits() - limitPayment >= 0:
            self.__FreeLimitToday -= limitPayment
            return True
        else:
            return False

    # списываем с дневного лимита 
    def set_decBalance(self, payment = 1):
        if self.get_balance() - payment >= 0:
            self.__balance -= payment
            return True
        else:
            return False

    # Оплата операции
    def pay(self, payment: float):
        ResultOperation = False # все плохо, если ничто этого не изменит

        # Если пользователь не исчерпал бесплатные операции на день - он ничего не платит
        # Если исчерпал - платит
        if self.set_decLimints(payment):
            ResultOperation = True
            Operation = 'Списание в счёт суточного лимита'
        else:    
            if self.set_decBalance(payment):
                ResultOperation = True
                Operation = 'Списание с баланса счета' 

            else:
                Operation = 'Недостаточно срдеств на счете' 
                print(f"Пополните баланс или дождитесь возобновления суточного лимита обращений. \nДля выполнения операции не хватает {abs(self.get_balance() - payment)} ед.")
            
        self.__Operations.update(Date = datetime.datetime.now(), 
                                Operation = Operation, 
                                Val = -payment,
                                Success = ResultOperation)

        return ResultOperation
            