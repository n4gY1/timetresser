from django import forms

from service_provider.models import ServiceProvider, ServiceProviderOpeningHours, ServiceProviderPicture


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = '__all__'
        exclude = ('user_profile', 'expired_date')

        labels = {
            'banner_picture': 'Borítókép',
            'phone_number': 'Telefonszám',
            'description': 'Leírás',
            'prices': 'Árlista',
            'booking_date_nr': 'Előre foglalható napok maximum száma',
            'booking_time_interval': 'Foglalások közötti időkülönbség (perc)',
            'name': 'Üzlet neve',
            'type': 'Fő profil'
        }

    def __init__(self, *args, **kwargs):
        super(ServiceProviderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'


class ServiceProviderOpeningHoursForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderOpeningHours
        fields = ['day', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(ServiceProviderOpeningHoursForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'


class ServiceProviderPictureForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderPicture
        fields = ['image',]

    def __init__(self, *args, **kwargs):
        super(ServiceProviderPictureForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'