#!/bin/bash

api_name=shugarev1974/check_order_api_catboost
file_settings=./check_order_api_catboost/settings.py

# заменить 'HOST': 'localhost'  на 'HOST': 'db'
# sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" $file_settings

#  Не устанавливать Debug режим
sed -i "s/DEBUG = True/DEBUG = False/g" $file_settings


# удаление прдедидущего образа проекта
#docker rmi ${api_name}

# создание нового образа из проекта
docker build -t ${api_name} .

# залогиниться в dockerhub репозитории
#docker login

# запушить изменения в репозиторий
#docker push ${api_name}

# Обратная замена 'HOST': 'db' на 'HOST': 'localhost'
# sed -i "s/'HOST': 'db'/'HOST': 'localhost'/g" $file_settings

sed -i "s/DEBUG = False/DEBUG = True/g" ${file_settings}
