import uuid

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_decode

from account.forms import UserForm, UserProfileForm
from account.models import User, UserProfile
from timetresses.utils import send_verification_email


# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                auth.login(request, user)
            except Exception as e:
                print(e)

            return redirect('home')
        else:
            messages.success(request, "Sorry, not valid username and password or "
                                      "not activated user")
            print(email, password)
            return redirect('login')

    return render(request, 'account/login.html')


@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')


def register(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            if request.POST['password'] == request.POST['confirm_password']:

                user = form.save(commit=False)
                user.username = str(uuid.uuid4())[0:10]
                user.email = request.POST['email'].lower()
                user.set_password(request.POST['password'])
                user.save()

                send_verification_email(request, user)

                messages.success(request, "Sikeres regisztráció. Megerősítő email elküldve")
                return redirect('login')
            else:
                messages.warning(request, "A jelszavak nem egyeznek")
        else:
            messages.warning(request, "Hiba történt: " + form.errors)

    context = {
        'form': form
    }

    return render(request, 'account/register.html', context)


def activate(request, uidb64, token):
    print(uidb64, token)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except Exception as e:
        print(e)
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Sikeres aktiválás')
        return redirect('login')
    else:
        messages.error(request, 'Nem érvényes a link')
        return redirect('login')


@login_required(login_url="login")
def settings(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Sikeres mentés")
            return redirect('settings')

    context = {
        "form": form,
        "user_profile": user_profile
    }

    return render(request, 'account/user_settings.html', context)
