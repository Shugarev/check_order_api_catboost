python manage.py runserver

# save environment settings to file.
pip freeze > requirements.txt

Обновили версии пакетов на начало 2021 года.

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

http://192.168.0.105:8037/api/v3/check_order/

В docker compose можно задать порт по которому будет слушаться.

Если мы не хотим пушить образ в докер репозиторий, то используем команды для сохранения и загрузки образа:
docker save -o /catboost-docker.tar shugarev1974/check_order_api_catboost

Для записи на сервер поменять пользователя:
sudo chown sergey:sergey catboost-docker.tar
скопировать файл на сервер и распаковать образ.
docker load -i catboost-docker.tar

Список поддерживаемых алгоритмов(вставляется в url вместо xgboost):
    'catboost','adaboost', 'gausnb', 'decisiontree', 'gradientboost', 'logregression', 'linear_sgd','xgboost, lightgbm',
    'pytorch'.

Все модели сохраняется через joblib метод, как dictionary:
conf_model = {'profile': model, 'algorithm_name': 'pytorch', 'factor_list': COL_FACTORS,
'replaced_values': replaced_values, 'scaler_params': scaler_params}

В 'replaced_values' - нужно передавать значение 'default', если оно отсутствует то в данных остаются поля с 'Na'.

Для 'catboost' обязательно наличие поля 'numeric_features' в сохранненной модели.

Для 'pytorch' обязательно поле 'scaler_params'.

Для работы 'pytorch' нужно добавлять модель в файл pytorch_models.py. Пример модели в классе 'MLP'. Файл
pytorch_models.py должен быть в папке 'media' докер-контейнера.
-----------------------------------------------------------------------------------------------------------
Для тестирования приложения на сервере по локальной запустить curl-api-catboost.sh
Для тестирования приложения на сервере скрипт curl-api-catboost.sh нужно запускать под sudo

{"config": {"profile": "xgb_3-80-035_2021-01-26"},
"data": {
"amount": "158.85",
"bin": "510932",
"day_of_week": "2",
"hour": "00",
"bank_currency": "840",
"is_city_resolved": "1",
"latitude": "undef",
"is_gender_undefined": "1",
"longitude": "undef",
"phone_2_norm": "20"
}
}
probability: 0.24286704

{"config": {"profile": "cat_3-75-015_seed_45_2021-01-26"},
"data": {
"amount": "158.85",
"bank_currency": "840",
"bin": "510932",
"day_of_week": "2",
"hour": "00",
"is_city_resolved": "1",
"is_gender_undefined": "1",
"latitude": "undef",
"longitude": "undef",
"phone_2_norm": "20"}
}
probability: 0.02343293

{"config": {"profile": "pytorch_30-09-001_2021-01-26"},
"data": {
"latitude": "undef",
"bank_currency": "840",
"bin": "510932",
"count_months_to_end_card": "19",
"day_of_week": "2",
"hour": "00",
"is_city_resolved": "1",
"is_gender_undefined": "1",
"longitude": "undef",
"amount": "158.85",
"phone_2_norm": "20"
}
}
probability: 0.03023967519402504
