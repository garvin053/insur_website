from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'nationality', 'first_name', 'last_name', 'city', 'emer_contact_num', 'emer_contact_person',
            'gender',
            'zipcode', 'street', 'password2', 'password1')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
