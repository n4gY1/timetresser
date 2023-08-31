from django.urls import path

from account.views import login, register, activate, settings, logout

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('settings/',settings,name="settings")


]
