import uuid

from django.db import models

from account.models import UserProfile

SERVICE_TYPE = (
    ('salon', "Fodrászat"),
    ('nails', "Műkörmös"),
    ('solarium', "Szolárium"),
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

    expired_date = models.DateTimeField()

    description = models.TextField(blank=True, null=True)

    prices = models.TextField(blank=True, null=True)

    booking_date_nr = models.SmallIntegerField(default=7)
    booking_time_interval = models.SmallIntegerField(default=30)

    type = models.CharField(max_length=15, choices=SERVICE_TYPE, default=SERVICE_TYPE[0])

    def __str__(self):
        return self.name


class ServiceProviderPicture(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_providers_pictures')


class ServiceProviderOpeningHours(models.Model):
    day = models.CharField(max_length=1, choices=OPENING_HOURS_DAYS)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE,related_name="opening")
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "day: " + self.day + " start: " + str(self.start_time) + " end: " + str(self.end_time)