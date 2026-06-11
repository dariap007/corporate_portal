from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField('Название отдела', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    STATUS_WORKS = 'works'
    STATUS_VACATION = 'on_vacation'
    STATUS_DISMISSED = 'dismissed'

    STATUS_CHOICES = [
        (STATUS_WORKS, 'Работает'),
        (STATUS_VACATION, 'В отпуске'),
        (STATUS_DISMISSED, 'Уволен'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Пользователь',
    )
    full_name = models.CharField('ФИО', max_length=150)
    position = models.CharField('Должность', max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Отдел',
    )
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=30, blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_WORKS,
    )
    additional_contact = models.TextField('Дополнительные контакты', blank=True)

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class NewsCategory(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
        verbose_name='Категория',
    )
    content = models.TextField('Текст новости')
    publication_date = models.DateField('Дата публикации', default=timezone.localdate)
    is_important = models.BooleanField('Важная новость', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-publication_date', '-created_at']

    def __str__(self):
        return self.title

class DocumentCategory(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория документа'
        verbose_name_plural = 'Категории документов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField('Название документа', max_length=200)
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='Категория',
    )
    description = models.TextField('Описание', blank=True)
    link = models.URLField('Ссылка')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['title']

    def __str__(self):
        return self.title

class CorporateServiceLink(models.Model):
    title = models.CharField('Название сервиса', max_length=100)
    description = models.TextField('Описание', blank=True)
    url = models.URLField('Ссылка')
    icon_name = models.CharField('Иконка или короткая метка', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Корпоративный сервис'
        verbose_name_plural = 'Корпоративные сервисы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Ticket(models.Model):
    TYPE_IT = 'it'
    TYPE_HR = 'hr'
    TYPE_ADMINISTRATIVE = 'administrative'
    TYPE_ACCESS = 'access'
    TYPE_OTHER = 'other'

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_REJECTED = 'rejected'

    TYPE_CHOICES = [
        (TYPE_IT, 'IT'),
        (TYPE_HR, 'HR'),
        (TYPE_ADMINISTRATIVE, 'Административная'),
        (TYPE_ACCESS, 'Доступ'),
        (TYPE_OTHER, 'Другое'),
    ]

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Низкий'),
        (PRIORITY_MEDIUM, 'Средний'),
        (PRIORITY_HIGH, 'Высокий'),
    ]

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Автор',
    )
    title = models.CharField('Тема заявки', max_length=200)
    description = models.TextField('Описание')
    ticket_type = models.CharField('Тип заявки', max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(
        'Приоритет',
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def status_badge_class(self):
        classes = {
            self.STATUS_NEW: 'text-bg-primary',
            self.STATUS_IN_PROGRESS: 'text-bg-warning',
            self.STATUS_COMPLETED: 'text-bg-success',
            self.STATUS_REJECTED: 'text-bg-secondary',
        }
        return classes.get(self.status, 'text-bg-primary')
