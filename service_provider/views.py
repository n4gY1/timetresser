import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from account.models import UserProfile
from booking.models import Booking
from rating.forms import RatingForm
from rating.models import Rating
from service_provider.forms import ServiceProviderForm, ServiceProviderOpeningHoursForm, ServiceProviderPictureForm
from service_provider.models import ServiceProvider, ServiceProviderOpeningHours, ServiceProviderPicture

import pytz

from service_provider.utils import FreeBookingTimes, get_service_providers_sorted_by_user_bookings


# Create your views here.
def home(request):
    #objs = ServiceProvider.objects.filter(expired_date__gte=datetime.datetime.now())

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        objs = get_service_providers_sorted_by_user_bookings(user_profile)
    else:
        objs = ServiceProvider.objects.filter(expired_date__gte=timezone.now())

    if request.method == "GET" and request.GET.get('search'):
        search_text = request.GET.get("search")
        objs = objs.filter(city__contains=search_text) | objs.filter(name__contains=search_text)
    context = {
        "objs": objs
    }

    return render(request, 'service_provider/list_service_provider.html', context)


@login_required(login_url="login")
def service_settings(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)


    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)
    form = ServiceProviderForm(instance=service_provider)
    current_date = datetime.datetime.now(tz=pytz.timezone('Europe/Budapest'))
    today = datetime.datetime(year=current_date.year, month=current_date.month,
                              day=current_date.day, hour=0, minute=0,
                              )  # mai nap
    tomorrow = today + datetime.timedelta(days=1)
    after_tomorrow = tomorrow + datetime.timedelta(days=1)

    opening_hour_form = ServiceProviderOpeningHoursForm()

    open_hours = service_provider.opening.all().order_by('day')

    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, request.FILES, instance=service_provider)
        opening_hour_form = ServiceProviderOpeningHoursForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Módosítás sikeres")

        if opening_hour_form.is_valid():
            day = opening_hour_form.cleaned_data['day']
            start_ime = opening_hour_form.cleaned_data['start_time']  # 7:50
            end_time = opening_hour_form.cleaned_data['end_time']


            opening_day = ServiceProviderOpeningHours.objects.filter(
                day=day, service_provider=service_provider)
            if opening_day:
                tmp = ServiceProviderOpeningHoursForm(request.POST, instance=opening_day[0])
                tmp.save()
                messages.success(request,"Nyitva tartás módosítása sikeres")
            else:
                ServiceProviderOpeningHours.objects.create(
                    day=day,
                    start_time=start_ime,
                    end_time=end_time,
                    service_provider=service_provider
                )
                messages.success(request, "Nyitva tartás rögzítése sikeres")
        return redirect('service_settings')

    if service_provider:
        context = {
            "service_provider": service_provider,
            "form": form,
            "today_booking": service_provider.bookings.all().filter(start_time__gte=today,
                                                                    end_time__lte=tomorrow).count(),
            "tomorrow_booking": service_provider.bookings.all().filter(start_time__gte=tomorrow,
                                                                       end_time__lte=after_tomorrow).count(),

            "open_hours": open_hours,
            "opening_hour_form": opening_hour_form
        }
        return render(request, 'service_provider/service_settings.html', context)
    else:
        return HttpResponseServerError("Nincs jogosultsága a megtekintéshez")


def list_service_providers(request, serv_type):
    objs = ServiceProvider.objects.filter(type=serv_type,expired_date__gte=datetime.datetime.now())
    context = {
        "objs": objs,

    }

    return render(request, 'service_provider/list_service_provider.html', context)


def view_service(request, service_slug):
    current_date = datetime.datetime.now(tz=pytz.timezone('Europe/Budapest'))

    try:
        obj = ServiceProvider.objects.get(slug=service_slug, expired_date__gte=current_date)
    except Exception as e:
        messages.warning(request,"Nem található ilyen üzlet")
        return redirect('home')

    current_date = datetime.datetime(year=current_date.year, month=current_date.month,
                                     day=current_date.day, hour=0, minute=0,
                                     ) + datetime.timedelta(days=1)  # holnapi nap

    two_day_later = current_date + datetime.timedelta(days=2)  # 2 nap múlva
    # igazából a holnapi nap

    # referencia képek
    refer_pictures = obj.refer_pictures.all()

    # szavazások
    ratings = obj.service_ratings.all().order_by('-created_at')

    # rating form
    rating_form = RatingForm()

    max_booking_date = obj.booking_date_nr
    max_time_interval = obj.booking_time_interval

    free_times = []

    for i in range(1, max_booking_date):
        week_day = (current_date.weekday() + 1)  # így kapjuk meg a magyar hét napját (vasárnap 0 ik)
        # it ha vasarnapra esik, akkor at allitjuk 0-ra, alias vasarnapra

        open_times = obj.opening.all().filter(day=week_day)
        # megnézzük a hét napját és az ahhoz tartozó nyitva tartást
        free_booking_times = FreeBookingTimes(current_date)

        for ot in open_times:
            free_booking_times.set_opening_hours(ot.start_time, ot.end_time)

            # idointervallum szerinti bontás
            start_open = datetime.datetime(
                year=current_date.year, month=current_date.month, day=current_date.day,
                hour=ot.start_time.hour, minute=ot.start_time.minute
            )

            end_open = datetime.datetime(
                year=current_date.year, month=current_date.month, day=current_date.day, hour=ot.end_time.hour,
                minute=ot.end_time.minute
            )

            # megyunk addig a megadott intervallum alapján amíg el nem fogy
            while start_open < end_open:
                tmp = start_open + datetime.timedelta(minutes=max_time_interval)

                booking = Booking.objects.filter(
                    Q(service=obj, is_accept=True) &
                    Q(start_time__lte=start_open, end_time__gt=tmp) |
                    Q(start_time__gte=start_open, end_time__lte=tmp) |
                    Q(start_time__gte=start_open, end_time__gte=tmp, start_time__lte=tmp) |
                    Q(start_time__lte=start_open, end_time__lte=tmp, end_time__gte=start_open)
                )
                if not booking:
                    free_booking_times.add_free_time(start_open)

                start_open = tmp
            free_times.append(free_booking_times)

        # itt adunk hozzá még egy napot
        current_date = current_date + datetime.timedelta(days=1)

    open_hours = obj.opening.all().order_by("day")

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_profile = get_object_or_404(UserProfile, user=request.user)
            try:
                exist_obj = Rating.objects.get(user_profile=user_profile, service_provider=obj)
                rating_form = RatingForm(request.POST, instance=exist_obj)
                if rating_form.is_valid():
                    rating_form.save()
                    messages.success(request,"Vélemény módosítása sikeres")
                    rating_form = RatingForm()
            except Exception as e:
                rating_form = RatingForm(request.POST)
                print(e)
                if rating_form.is_valid():
                    f = rating_form.save(commit=False)
                    f.user_profile = user_profile
                    f.service_provider = obj
                    f.save()
                    rating_form = RatingForm()
                    messages.success(request,"Vélemény rögzítése sikeres")
                else:
                    print(rating_form.errors)

        else:
            messages.success(request, "Véleményt csak bejelentkezett felhasználó rögzíthet")

    context = {
        "obj": obj,
        "open_hours": open_hours,
        "free_times": free_times,
        "refer_pictures": refer_pictures,
        "ratings": ratings,
        "rating_form": rating_form
    }
    return render(request, 'service_provider/view_service.html', context)


@login_required(login_url="login")
def delete_opening_hour(request, pk):
    opening_hour = get_object_or_404(ServiceProviderOpeningHours, pk=pk)
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)
    if opening_hour.service_provider == service_provider:
        print("törlésre jogosult")
        opening_hour.delete()
        messages.success(request, "Nyitva tartás törölve")

    else:
        print("not torles")
        messages.warning(request, "Nincs jogosultsága a törléshez")
    return redirect('service_settings')


@login_required(login_url="login")
def settings_refer_picture(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)

    refer_picture_form = ServiceProviderPictureForm()
    print()
    if request.method == 'POST':
        refer_picture_form = ServiceProviderPictureForm(request.POST, request.FILES)
        if service_provider.refer_pictures.count() >= 6:
            messages.warning(request,"Túllépte a képek feltöltésének maximális számát!")
            return redirect('settings_refer_picture')
        if refer_picture_form.is_valid():
            obj = refer_picture_form.save(commit=False)
            obj.service_provider = service_provider
            obj.save()
            messages.success(request, "Kép feltöltése sikeres")

    refer_pictures = service_provider.refer_pictures.all()

    context = {
        "refer_pictures": refer_pictures,
        "form": refer_picture_form,
    }
    return render(request, 'service_provider/refer_pictures.html', context)


@login_required(login_url="login")
def delete_refer_picture(request, pk):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    service_provider = get_object_or_404(ServiceProvider, user_profile=user_profile)
    picture = get_object_or_404(ServiceProviderPicture, pk=pk)
    if picture.service_provider.user_profile == user_profile:
        picture.delete()
        messages.success(request, "Kép sikeresen törölve")
    else:
        messages.warning(request, "Nincs jogosultsága a kép törléséhez")
    return redirect('settings_refer_picture')
