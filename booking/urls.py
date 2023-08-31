from django.urls import path

from booking.views import add_booking, list_not_accept_booking, show_not_accept_booking, list_accept_booking, \
    create_guest_booking

urlpatterns = [
    path('date/<slug:service_provider_slug>/<str:selected_date>/', add_booking,name="add_booking"),
    path('list_not_accept_booking/',list_not_accept_booking,name='list_not_accept_booking'),
    path('list_accept_booking/',list_accept_booking,name='list_accept_booking'),
    path('show_not_accept_booking/<int:pk>/',show_not_accept_booking,name="show_not_accept_booking"),
    path('create_guest_booking',create_guest_booking,name="create_guest_booking")
]