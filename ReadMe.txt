Problems:
i:
python manage.py runserver
error
cannot import name 'RemovedInDjango30Warning'

Comment out the following line:
from django.utils.deprecation import RemovedInDjango30Warning
/home/sergey/anaconda3/lib/python3.6/site-packages/00
/home/sergey/anaconda3/lib/python3.6/site-packages/django/contrib/staticfiles/templatetags/staticfiles.py

/home/sergey/PycharmProjects/VirtualEnv/env-catboost/lib/python3.6/site-packages/django/contrib/staticfiles/templatetags/staticfiles.py

ii:
# before start test in file api/urls.py comment line
# app_name = 'api'

# save environment settings to file.
pip freeze > requirements.txt
python  manage.py test api

path_to_env= ~/PycharmProjects/VirtualEnv/env-catboost/bin/activate


