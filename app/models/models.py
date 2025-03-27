# Простой класс для хранения модели и ее обще описательных характеристик
import random

class MLmodel:
    def __init__(self, model, name: str, version: str, description: str,):
        self.model = model # сама модель
        self.name = name # Название модели
        self.version = version # Версия модели
        self.description = description # Описательная характеристика модели

    def __str__(self):
        print(f"{self.model} \n" \
               f"Название: {self.name} \n"  \
               f"Версия: {self.version} \n" \
               f"Описание: {self.description}")
        


 # Наследуемый класс модели для учета ее параметров использования
class UsableModel(MLmodel):
    def __init__(self, model: MLmodel, name: str, version: str, description: str, price: float):
        super().__init__(model, name, version, description)
        self.price = price # Стоимость использования модели

        self.StatusOperation = None # Статус последнего запуска
        self.Result = None # Результаты работы модели

    def run(self):
        # Запускаем модель и сообщаем о статусе
        self.StatusOperation = bool(random.randint(0, 1)) # Успешность модели пока рандомна - может работать, а может нет
        print('| Модель сработала: ', self.StatusOperation, '|\n' )
        self.Result = 'Результаты работы модели'    

    def __str__(self):
        super().__str__()
        print(f"Стоимость: {self.price} \n"  \
              f"Статус последнего запуска: {self.StatusOperation}")        