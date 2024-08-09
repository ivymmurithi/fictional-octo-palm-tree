from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'accounts', views.AccountViewSet, basename='accounts')


urlpatterns = [
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('send/', views.send, name="send"),
    path('', include(router.urls)),
]