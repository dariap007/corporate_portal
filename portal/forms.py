import re

from django import forms
from django.contrib.auth.models import User

from .models import CorporateServiceLink, Department, Document, EmployeeProfile, News, Ticket


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


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'category', 'content', 'publication_date', 'is_important']
        labels = {
            'title': 'Заголовок',
            'category': 'Категория',
            'content': 'Текст новости',
            'publication_date': 'Дата публикации',
            'is_important': 'Важная новость',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'publication_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = EmployeeProfile
        fields = [
            'username',
            'password',
            'full_name',
            'position',
            'department',
            'email',
            'phone',
            'status',
            'additional_contact',
        ]
        labels = {
            'full_name': 'ФИО',
            'position': 'Должность',
            'department': 'Подразделение',
            'email': 'Email',
            'phone': 'Телефон',
            'status': 'Статус',
            'additional_contact': 'Дополнительные контакты',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'additional_contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['full_name', 'position', 'department', 'email', 'phone', 'status', 'additional_contact']
        labels = {
            'full_name': 'ФИО',
            'position': 'Должность',
            'department': 'Подразделение',
            'email': 'Email',
            'phone': 'Телефон',
            'status': 'Статус',
            'additional_contact': 'Дополнительные контакты',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'additional_contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = profile.email
        if commit:
            profile.user.save()
            profile.save()
        return profile


class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'category', 'description', 'link']
        labels = {
            'title': 'Название документа',
            'category': 'Категория',
            'description': 'Описание',
            'link': 'Ссылка',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'admin_comment']
        labels = {
            'status': 'Статус',
            'admin_comment': 'Комментарий администратора',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        labels = {
            'name': 'Название подразделения',
            'description': 'Описание',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CorporateServiceLinkAdminForm(forms.ModelForm):
    class Meta:
        model = CorporateServiceLink
        fields = ['title', 'description', 'url', 'icon_name']
        labels = {
            'title': 'Название сервиса',
            'description': 'Описание',
            'url': 'Ссылка',
            'icon_name': 'Короткая метка',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'icon_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
