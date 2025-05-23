from django import forms
from .models import Booking, Car, CarModel
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < date.today():
                raise forms.ValidationError('Дата начала не может быть в прошлом.')
            if end_date <= start_date:
                raise forms.ValidationError('Дата окончания должна быть позже даты начала.')
        return cleaned_data

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_model', 'year', 'transmission', 'fuel_type', 'min_price', 'max_price', 'current_price', 'photo', 'status']
        widgets = {
            'car_model': forms.Select(),
            'transmission': forms.Select(),
            'fuel_type': forms.Select(),
            'status': forms.Select(),
            'photo': forms.ClearableFileInput(),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введите действительный email адрес.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user