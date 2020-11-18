from django.urls import path

from . import views

#app_name = 'api'

urlpatterns = [
    path('v2/check_order/', views.get_order_probability, name='get_order_probability')
]