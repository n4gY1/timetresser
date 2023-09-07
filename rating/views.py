from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from account.models import UserProfile
from rating.models import Rating


# Create your views here.
# a felvitel a service_provider.views fájlban van
@login_required(login_url='login')
def delete_my_rating(request,pk):
    user_profile = get_object_or_404(UserProfile,user=request.user)
    rating = get_object_or_404(Rating,pk=pk)
    if rating.user_profile == user_profile:
        rating.delete()
        messages.success(request,"Vélemény törölve")
        return redirect('settings')
    else:
        messages.warning(request,"Nincs jogosultsága a törléshez")
        return redirect('settings')