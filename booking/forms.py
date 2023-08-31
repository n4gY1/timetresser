from django import forms

from booking.models import Booking


class BookingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-primary', 'rows': 5}),
                                  label="Kérjük adja meg az igényelt szolgáltatás legpontosabb leírását")

    class Meta:
        model = Booking
        fields = ["description"]

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary'


class BookingGuestForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-primary', 'rows': 5}),
                                  label="Kérjük adja meg az igényelt szolgáltatás legpontosabb leírását")
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control bg-primary', 'type': 'datetime-local'
    }), label='Kezdési időpont')

    class Meta:
        model = Booking
        fields = ["start_time", "description", "length"]

    def __init__(self, *args, **kwargs):
        super(BookingGuestForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary'


class BookingManageForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-primary', 'rows': 3,
                                                               'readonly': True}),
                                  label="Leírás")

    accept_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-primary', 'rows': 3}),
                                         label="Hozzáfűzés")

    length = forms.IntegerField(widget=forms.NumberInput(attrs={'required': True, 'min': 10,
                                                                'class': 'form-control bg-primary',
                                                                'placeholder': 'Saccolt időtartam percben'}),
                                label="Időtartam percben")

    is_accept = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check', 'onclick': 'ClickCheckBox()'}),
        label="Elfogadva?", required=False)

    class Meta:
        model = Booking
        fields = ["description", "length", "is_accept", "accept_description"]
