from models.user import User
from models.models import UsableModel
import random


if __name__ == "__main__":

    # Инициируем модели
    CurrModel_1 = UsableModel('', 'Убиватор-3000', '1.01', 'Офигенская модель, прям всем советую только ее',
                            price = 1)

    CurrModel_2 = UsableModel('', 'УльтраУбиватор-9000', '3.33', 'Еще более крутая и дорогая модель.',
                            price = 2)
    
    # Для демонстрации сделаем выбор модели случайным образом
    if bool(random.randint(0, 1)): CurrModel = CurrModel_1
    else: CurrModel = CurrModel_2


    # Создание пользователя
    CurrentUser = User(name = 'dmagog',
                    email = 'georgy-mamarin@mail.ru',
                    role = 1,
                    startbalance = 5,
                    FreeLimitPerDay = 3)

    print(CurrentUser)


    
    for _ in range(0,5):
        #Пользователь вызывает модель
        CurrentUser.useModel(model = CurrModel, 
                            payment = CurrModel.price)

    
    print()
    print('Балланс = ', CurrentUser.billing.get_balance())
    print('Бесплатных операций осталось = ', CurrentUser.billing.get_limits())
    print('Последняя операция = ', CurrentUser.history.get_lastOperationDate())
    print('Всего операций = ', CurrentUser.history.get_OperationAll())
    print('Операций cегодня = ', CurrentUser.history.get_OperationToday())

    print()
    print(CurrentUser.history.get())

    print()
    print(CurrentUser.billing.get_operations())