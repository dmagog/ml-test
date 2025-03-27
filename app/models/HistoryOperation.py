import numpy as np
import pandas as pd
import datetime



class HistoryOperation:
    
    def __init__(self):
        self.LastOperationDate = np.nan # Дата последней удачной операции
        self.HistoryOperation = pd.DataFrame(columns=['Date', 'Operation', 'Success']) # Список всех операций и дата свершения
        
        self.OperationAll = 0 # Сколько операций сделано за все время
        self.OperationToday = 0 # сколько операций сделано сегодня

        self.Initiation = False # Прошел ли пользователь инициацию первым успешным использованием сервисв


    def get(self):
        return self.HistoryOperation


    def update(self, Date, Operation: str, Success: bool):
        self.set_Initiation()

        LastPos = len(self.get())
        self.HistoryOperation.loc[LastPos, 'Date'] = Date
        self.HistoryOperation.loc[LastPos, 'Operation'] = Operation
        self.HistoryOperation.loc[LastPos, 'Success'] = Success

        self.set_lastOperationDate()

        self.OperationToday += 1
        self.OperationAll += 1


    def get_lastOperationDate(self):
        return self.LastOperationDate
    
    def set_lastOperationDate(self, OperationDate = datetime.datetime.now()):
        self.LastOperationDate = OperationDate


    def get_OperationAll(self):
        return self.OperationAll

    def get_OperationToday(self):
        return self.OperationToday


    def set_OperationToday(self, Num = 0):
        self.OperationToday = Num

    def set_Initiation(self):
        self.Initiation = True
    
    def get_Initiation(self):
        return self.Initiation