from django.urls import path, include

from service_provider.views import home, service_settings, list_service_providers, view_service, delete_opening_hour, \
    settings_refer_picture, delete_refer_picture

urlpatterns = [
    path('', home, name='home'),
    path('service_settings/', service_settings, name='service_settings'),
    path('services/<slug:serv_type>/', list_service_providers, name="list_service_providers"),

    path('view_service/<slug:service_slug>/', view_service,name='view_service'),
    path('delete_opening_hour/<int:pk>',delete_opening_hour,name='delete_opening_hour'),
    path('settings_refer_picture/',settings_refer_picture,name='settings_refer_picture'),
    path('delete_refer_picture/<int:pk>',delete_refer_picture,name='delete_refer_picture'),
]
