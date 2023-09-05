from django import forms

from rating.models import Rating


class RatingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': "3"}))

    class Meta:
        model = Rating
        fields = ['rate', 'description']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-primary text-light'
