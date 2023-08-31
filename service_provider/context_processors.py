from account.models import User, UserProfile
from service_provider.models import SERVICE_TYPE, ServiceProvider


# ha a user be van jelentkezve, megnézi társul e hozzá szolgáltatás
def get_context_processors(request):
    is_provider = False
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if ServiceProvider.objects.filter(user_profile=user_profile).exists():
                is_provider = True
                sp = ServiceProvider.objects.get(user_profile=user_profile)
                return {
                    "SERVICE_TYPES": SERVICE_TYPE,
                    # az adatbázisból lekérdezés, hány "szerviz" tag [chooicefiel] van (service type)
                    "is_provider": is_provider,
                    "not_accepted_booking": sp.bookings.all().filter(is_accept=False).count()
                }
        except Exception as e:
            print("nem szolgaltatls",e)

    return {
        "SERVICE_TYPES": SERVICE_TYPE,
        # az adatbázisból lekérdezés, hány "szerviz" tag [chooicefiel] van (service type)
        "is_provider": is_provider,
    }
