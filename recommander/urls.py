from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.recommend_products, name='recommend_products'),
]
