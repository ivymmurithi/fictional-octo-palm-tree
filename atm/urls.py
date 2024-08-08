from . import views
from django.urls import path

urlpatterns = [
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('send/', views.send, name="send"),
]