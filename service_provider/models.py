import uuid

from django.db import models
from django.db.models import Sum, Avg

from account.models import UserProfile

SERVICE_TYPE = (
    ('salon', "Fodrászat"),
    ('nails', "Műkörmös"),
    ('solarium', "Szolárium"),
    ('kozmetikus', "Kozmetikus"),
)

OPENING_HOURS_DAYS = (
    ('1', 'Hétfő'),
    ('2', 'Kedd'),
    ('3', 'Szerda'),
    ('4', 'Csütörtök'),
    ('5', 'Péntek'),
    ('6', 'Szombat'),
    ('7', 'Vasárnap'),
)


# Create your models here.


class ServiceProvider(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    slug = models.SlugField(blank=True, null=True, unique=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zip_code = models.SmallIntegerField()

    banner_picture = models.ImageField(upload_to='service_providers_banners')

    mobile = models.CharField(max_length=50)
    fb_link = models.URLField(blank=True,null=True)
    insta_link = models.URLField(blank=True,null=True)
    expired_date = models.DateTimeField()

    description = models.TextField(blank=True, null=True)


    prices = models.TextField(blank=True, null=True)

    booking_date_nr = models.SmallIntegerField(default=7)
    booking_time_interval = models.SmallIntegerField(default=30)

    type = models.CharField(max_length=15, choices=SERVICE_TYPE, default=SERVICE_TYPE[0])

    def __str__(self):
        return self.name

    def get_rating_value(self):
        obj = ServiceProvider.objects.get(id=self.id)

        avg = obj.service_ratings.all().aggregate(Avg('rate'))
        avg = avg['rate__avg'] if avg['rate__avg'] is not None else 0
        avg = int(avg)
        return avg

    def show_rating_stars(self):
        html = ""
        rating_value = self.get_rating_value()
        for i in range(1, 6):
            if i <= rating_value:
                html += '<i class="fa-solid fa-star text-warning"></i>'
            else:
                html += '<i class="fa-solid fa-star"></i>'

        return html


class ServiceProviderPicture(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE,related_name="refer_pictures")
    image = models.ImageField(upload_to='service_providers_pictures')


class ServiceProviderOpeningHours(models.Model):
    day = models.CharField(max_length=1, choices=OPENING_HOURS_DAYS)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE,related_name="opening")
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "day: " + self.day + " start: " + str(self.start_time) + " end: " + str(self.end_time)