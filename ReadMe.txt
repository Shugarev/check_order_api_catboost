python manage.py runserver

# save environment settings to file.
pip freeze > requirements.txt

python  manage.py test api
------------------------------------------------------------------------------------------------------------
открыть доступ для всех ip.

в settings.py установить:
    DEBUG = False

для запуска на сервере нужно:
- создать папку для сервиса
- в нее положить docker-compose.yml
- созадать поддиректорию media и положит в нее конфигурационный файл и файлы моделей.
- для поднятия сервиса выполнить docker-compose up
- пример url по которому произовдится проверка ордреа,

http://192.168.0.105:8000/api/v2/check_order/

В docker compose можно задать порт по которому будет слушаться.

Список поддерживаемых алгоритмов(вставляется в url вместо xgboost):
    'catboost','adaboost', 'gausnb', 'decisiontree', 'gradientboost', 'logregression', 'linear_sgd','xgboost, lightgbm'

Название 'catboost' модели должно начинаться с 'cat'

Модель 'catboost' сохраняется двумя типами через joblib метод, по дефолту:"<class 'catboost.core.CatBoostClassifier'>"
или как dictionary:{'profile': catboost.core.CatBoostClassifier, 'encode': encode_dict}
В encode_dict - в полях передаем параметры, которые потом можем использовать для корректной работы модели,
пример encode_dict
{'longitude': 78, 'latitude':34} тогда значения na в соответствующих колонках будут заменятся на 78 и 34.
Для совместимости 'django-sklearn-v2' и 'order-api-lignt', версии 'xgboost' и 'sklearn' оставили прежними.

