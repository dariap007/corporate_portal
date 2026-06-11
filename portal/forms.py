import re

from django import forms

from .models import EmployeeProfile, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'ticket_type', 'priority']
        labels = {
            'title': 'Тема заявки',
            'description': 'Описание',
            'ticket_type': 'Тип заявки',
            'priority': 'Приоритет',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'ticket_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['phone', 'additional_contact']
        labels = {
            'phone': 'Телефон',
            'additional_contact': 'Дополнительные контакты',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67',
                'inputmode': 'numeric',
                'maxlength': '18',
                'pattern': r'\+7 \([0-9]{3}\) [0-9]{3}-[0-9]{2}-[0-9]{2}',
                'title': 'Введите номер в формате +7 (999) 123-45-67',
                'autocomplete': 'tel',
                'required': 'required',
                'data-phone-mask': 'true',
            }),
            'additional_contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True
        if self.instance and self.instance.phone:
            self.initial['phone'] = self.format_phone(self.instance.phone)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = re.sub(r'\D', '', phone)

        if digits.startswith('8'):
            digits = '7' + digits[1:]

        if len(digits) != 11 or not digits.startswith('7'):
            raise forms.ValidationError('Введите номер телефона в формате +7 (999) 123-45-67.')

        return self.format_phone(digits)

    @staticmethod
    def format_phone(phone):
        digits = re.sub(r'\D', '', phone)

        if digits.startswith('8'):
            digits = '7' + digits[1:]

        if len(digits) != 11 or not digits.startswith('7'):
            return phone

        return f'+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}'
