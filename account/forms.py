from django import forms

from account.models import User, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-light text-dark'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light text-dark'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        labels = {
            'first_name': 'Vezetéknév',
            'last_name': 'Keresztnév',
            'email':'E-mail',
            'password': 'Jelszó',
            'confirm_password':'Jelszó megerősítése'
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'
            self.fields['password'].label = 'Jelszó'
            self.fields['confirm_password'].label = 'Jelszó megerősítése'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user',)

        labels = {
            'profile_picture': 'Profil kép',
            'phone_number': 'Telefonszám'
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'
