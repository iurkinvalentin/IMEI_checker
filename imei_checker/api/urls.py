from django.urls import path
from .views import IMEICheckView

urlpatterns = [
    path('check-imei/', IMEICheckView.as_view(), name='check_imei'),
]
