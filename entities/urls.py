from django.urls import path

from entities import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'entities', views.EntityViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/part', views.DetailPartView.as_view(), name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('api/entities/', views.EntityListAPIView.as_view()),
]
