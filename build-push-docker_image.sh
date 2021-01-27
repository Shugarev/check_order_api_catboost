#!/bin/bash

api_name=shugarev1974/check_order_api_catboost_v3
file_settings=./check_order_api_catboost/settings.py

project_data=data_for_testing
project_media=media

tmp_data=../tmp-data_for_testing
tmp_media=../tmp-media

pytorch_models=pytorch_models.py
init=__init__.py

# заменить 'HOST': 'localhost'  на 'HOST': 'db'
# sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" $file_settings

#  Не устанавливать Debug режим
sed -i "s/DEBUG = True/DEBUG = False/g" $file_settings


if [ -d ${tmp_data} ]; then rm -Rf ${tmp_data}; fi
mkdir -p ${tmp_data}
find ${project_data} -type f -print0 | xargs -0 mv -t ${tmp_data}

if [ -d ${tmp_media} ]; then rm -Rf ${tmp_media}; fi
mkdir -p ${tmp_media}
find ${project_media} -type f -print0 | xargs -0 mv -t ${tmp_media}

# move pytorch_models.py and __init__.py to media folder
mv ${tmp_media}/${pytorch_models} ${project_media}
mv ${tmp_media}/${init} ${project_media}

# удаление прдедидущего образа проекта
docker rmi ${api_name}

# создание нового образа из проекта
docker build -t ${api_name} .

# залогиниться в dockerhub репозитории
#docker login

# запушить изменения в репозиторий
#docker push ${api_name}

# Обратная замена 'HOST': 'db' на 'HOST': 'localhost'
# sed -i "s/'HOST': 'db'/'HOST': 'localhost'/g" $file_settings

sed -i "s/DEBUG = False/DEBUG = True/g" ${file_settings}

find ${tmp_data} -type f -print0 | xargs -0 mv -t ${project_data}
rmdir ${tmp_data}

find ${tmp_media} -type f -print0 | xargs -0 mv -t ${project_media}
rmdir ${tmp_media}