from django.db import models

from account.models import UserProfile
from service_provider.models import ServiceProvider


# Create your models here.
rating_value = (
    (1,'Nem ajánlom'),
    (2,'Tűrhető'),
    (3,'Átlagos'),
    (4,'Jó'),
    (5,'Kiválló')
)

class Rating(models.Model):
    rate = models.SmallIntegerField(choices=rating_value)
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="my_ratings")
    service_provider = models.ForeignKey(to=ServiceProvider, on_delete=models.CASCADE, related_name="service_ratings")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def get_rating_stars(self):
        html = ""
        for i in range(1, 6):
            if i <= self.rate:
                html += '<i class="fa-solid fa-star text-warning"></i>'
            else:
                html += '<i class="fa-solid fa-star"></i>'

        return html
