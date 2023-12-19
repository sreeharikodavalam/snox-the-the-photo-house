from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Event, UserSelfieRegistration


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['bride_name', 'groom_name', 'date', 'venue', 'note', 'cover_image', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError(_('Please enter a future date.'))
        return date


class UserSelfieRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserSelfieRegistration
        fields = ['user_name', 'email_id', 'mobile_number', 'selfie_image', 'selfie_embedding']

    def __init__(self, *args, **kwargs):
        super(UserSelfieRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['selfie_image'].required = False
        self.fields['selfie_embedding'].required = False
