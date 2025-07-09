import datetime
from itertools import groupby
from operator import itemgetter

import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from account.models import UserProfile, User
from booking.forms import BookingForm, BookingManageForm, BookingGuestForm
from booking.models import Booking
from service_provider.models import ServiceProvider
from timetresses.utils import send_accept_mail, send_not_accept_mail, send_new_booking_mail


@login_required(login_url='login')
def add_booking(request, selected_date, service_provider_slug):
    sp = get_object_or_404(ServiceProvider, slug=service_provider_slug)

    form = BookingForm()
    min_res = sp.booking_time_interval
    user_profile = get_object_or_404(UserProfile, user=request.user)
    selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d %H:%M:%S')
    current_date = timezone.now()
    current_date = timezone.datetime(year=current_date.year, month=current_date.month,
                                     day=current_date.day, hour=0, minute=0
                                     ) + datetime.timedelta(days=1)

    tmp = current_date + timezone.timedelta(minutes=min_res)
    """
    # a datetime és localizációs dátumok nem összeegyezehtősége miatt van hiba
    if sp.expired_date < current_date:
        messages.warning(request, "A szolgáltató licensze lejárt. Sajnos nem lehet nála foglalni")
        return redirect('home')
    """


    if request.method == "POST":
        bookings = Booking.objects.filter(
            Q(service=sp) &
            Q(start_time__lte=selected_date, end_time__gt=selected_date, end_time__lte=tmp) |
            Q(start_time__gte=selected_date, end_time__lte=tmp) |
            Q(start_time__gte=selected_date, end_time__gte=tmp, start_time__lte=tmp) |
            Q(start_time__lte=selected_date, end_time__lte=tmp, end_time__gte=selected_date)
        )

        if not bookings:
            selected_date = request.POST.get('selected_date')
            description = request.POST.get('description')
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d %H:%M:%S')
            try:
                booked = Booking.objects.create(
                    service=sp,
                    booked_user=user_profile,
                    start_time=selected_date,
                    description=description
                )
                send_new_booking_mail(request=request,booking=booked)
                messages.success(request, "Sikeres foglalás, elfogadáskor visszaigazoló email-t küldünk.")

                return redirect('view_service', service_slug=sp.slug)
            except Exception as e:
                messages.error(request, "Hiba történt " + str(e))
                print(e)
        else:
            messages.error(request, "Sajnos ez az időpont már időközben lefoglalásra került")
    context = {
        "form": form,
        "selected_date": selected_date,
        "service": sp
    }
    return render(request, "booking/add_booking.html", context)


@login_required(login_url='login')
def list_not_accept_booking(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)

    not_accepted_booking = service_provider.bookings.filter(is_accept=False)
    context = {
        "bookings": not_accepted_booking,
        "service_provider": service_provider,
    }

    return render(request, 'booking/not_accept_booking.html', context)


# ez mikor konkrétan az időpontra megyunk ra, megmutatja az időponthoz tartozó más közeli idopontokat is
@login_required(login_url='login')
def show_not_accept_booking(request, pk):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)
    booking = get_object_or_404(Booking, pk=pk)

    if booking.service != service_provider:
        messages.warning(request, "Önnek nincs jogosultsága a megtekintéshez")
        return redirect('home')

    form = BookingManageForm(instance=booking)

    neighbor_bookings = Booking.objects.filter(
        is_accept=True, service=service_provider, start_time__range=(
            booking.start_time + datetime.timedelta(minutes=-100),
            booking.start_time + datetime.timedelta(minutes=100)
        )
    )

    if request.method == 'POST':
        form = BookingManageForm(request.POST, instance=booking)
        if form.is_valid():
            tmp = form.save(commit=False)
            if tmp.is_accept:
                tmp.save()
                messages.success(request, "Foglalás elmentve")
                send_accept_mail(request, booking)

                return redirect('list_not_accept_booking')

            else:
                messages.warning(request, "Foglalás törölve")
                send_not_accept_mail(request, booking)
                tmp.delete()

                return redirect('home')

        else:
            print(form.errors)

    context = {
        "form": form,
        "user_profile": user_profile,
        "booking": booking,
        "neighbor_bookings": neighbor_bookings,
    }
    return render(request, 'booking/show_not_accept_booking.html', context)


@login_required(login_url='login')
def list_accept_booking(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)

    objs = service_provider.bookings.all().filter(
        start_time__gte=datetime.datetime.now() + datetime.timedelta(days=-1)
    ).order_by('start_time')

    objs = groupby(objs, key=lambda x: x.start_time.date())

    grouped_objs = []
    for date, group in objs:
        b = list(group)
        sorted_booking = sorted(b, key=lambda x: x.start_time.time())
        grouped_objs.append(
            {
                'date': date,
                'objs': sorted_booking
            }
        )

    print(grouped_objs)

    context = {
        'grouped_objs': grouped_objs
    }
    return render(request, 'booking/list_bookings.html', context)


@login_required(login_url='login')
def create_guest_booking(request):
    guest_user = User.objects.get(username="guest")
    guest_user_profile = get_object_or_404(UserProfile, user=guest_user)

    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)
    form = BookingGuestForm()
    if request.method == 'POST':
        try:
            form = BookingGuestForm(request.POST)
            booking = form.save(commit=False)
            booking.booked_user = guest_user_profile
            booking.service = service_provider
            booking.is_accept = True
            booking.save()
            messages.success(request,"Rögzítés sikeres")
            return redirect('list_accept_booking')
        except Exception as e:
            messages.warning(request,"Hiba történt" + e)
        print(booking)

    context = {
        'form': form
    }

    return render(request, 'booking/create_guest_booking.html', context)
