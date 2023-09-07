from django.urls import path

from rating.views import delete_my_rating

urlpatterns = [
    path('delete/<int:pk>/', delete_my_rating, name="delete_my_rating"),
]
