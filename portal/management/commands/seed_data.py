from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from portal.models import (
    CorporateServiceLink,
    Department,
    Document,
    DocumentCategory,
    EmployeeProfile,
    News,
    NewsCategory,
    Ticket,
)


class Command(BaseCommand):
    help = 'Creates demo data for the corporate portal.'

    def handle(self, *args, **options):
        departments = self.create_departments()
        users = self.create_users()
        self.create_employee_profiles(users, departments)
        news_categories = self.create_news_categories()
        self.create_news(news_categories)
        document_categories = self.create_document_categories()
        self.create_documents(document_categories)
        self.create_service_links()
        self.create_tickets(users['employee'])

        self.stdout.write(self.style.SUCCESS('Demo data has been created successfully.'))

    def create_departments(self):
        data = [
            (
                'IT-отдел',
                'Поддержка сотрудников, настройка рабочих мест и внутренних сервисов.',
            ),
            (
                'Отдел персонала',
                'Кадровые вопросы, адаптация сотрудников и внутренние коммуникации.',
            ),
            (
                'Административный отдел',
                'Офисные вопросы, пропуска, документы и хозяйственное обеспечение.',
            ),
        ]

        departments = {}
        for name, description in data:
            department, _ = Department.objects.update_or_create(
                name=name,
                defaults={'description': description},
            )
            departments[name] = department
        return departments

    def create_users(self):
        users_data = [
            {
                'username': 'admin',
                'password': 'admin12345',
                'email': 'admin@tritochki.local',
                'first_name': 'Анна',
                'last_name': 'Соколова',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'employee',
                'password': 'employee12345',
                'email': 'employee@tritochki.local',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'smirnova',
                'password': 'employee12345',
                'email': 'smirnova@tritochki.local',
                'first_name': 'Мария',
                'last_name': 'Смирнова',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'volkov',
                'password': 'employee12345',
                'email': 'volkov@tritochki.local',
                'first_name': 'Дмитрий',
                'last_name': 'Волков',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'kuznetsova',
                'password': 'employee12345',
                'email': 'kuznetsova@tritochki.local',
                'first_name': 'Елена',
                'last_name': 'Кузнецова',
                'is_staff': False,
                'is_superuser': False,
            },
            {
                'username': 'orlov',
                'password': 'employee12345',
                'email': 'orlov@tritochki.local',
                'first_name': 'Алексей',
                'last_name': 'Орлов',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        users = {}
        for item in users_data:
            user, created = User.objects.get_or_create(username=item['username'])
            user.email = item['email']
            user.first_name = item['first_name']
            user.last_name = item['last_name']
            user.is_staff = item['is_staff']
            user.is_superuser = item['is_superuser']
            user.set_password(item['password'])
            user.save()
            users[item['username']] = user

            action = 'created' if created else 'updated'
            self.stdout.write(f'User {item["username"]} {action}.')

        return users

    def create_employee_profiles(self, users, departments):
        profiles_data = [
            {
                'username': 'admin',
                'full_name': 'Соколова Анна Викторовна',
                'position': 'Администратор портала',
                'department': departments['IT-отдел'],
                'email': 'admin@tritochki.local',
                'phone': '+7 900 100-10-10',
                'status': EmployeeProfile.STATUS_WORKS,
                'additional_contact': 'Telegram: @admin_tritochki',
            },
            {
                'username': 'employee',
                'full_name': 'Петров Иван Сергеевич',
                'position': 'Специалист по продажам',
                'department': departments['Административный отдел'],
                'email': 'employee@tritochki.local',
                'phone': '+7 900 200-20-20',
                'status': EmployeeProfile.STATUS_WORKS,
                'additional_contact': 'Telegram: @petrov',
            },
            {
                'username': 'smirnova',
                'full_name': 'Смирнова Мария Павловна',
                'position': 'HR-специалист',
                'department': departments['Отдел персонала'],
                'email': 'smirnova@tritochki.local',
                'phone': '+7 900 300-30-30',
                'status': EmployeeProfile.STATUS_WORKS,
                'additional_contact': '',
            },
            {
                'username': 'volkov',
                'full_name': 'Волков Дмитрий Андреевич',
                'position': 'Системный администратор',
                'department': departments['IT-отдел'],
                'email': 'volkov@tritochki.local',
                'phone': '+7 900 400-40-40',
                'status': EmployeeProfile.STATUS_WORKS,
                'additional_contact': 'Внутренний номер: 104',
            },
            {
                'username': 'kuznetsova',
                'full_name': 'Кузнецова Елена Игоревна',
                'position': 'Офис-менеджер',
                'department': departments['Административный отдел'],
                'email': 'kuznetsova@tritochki.local',
                'phone': '+7 900 500-50-50',
                'status': EmployeeProfile.STATUS_VACATION,
                'additional_contact': '',
            },
            {
                'username': 'orlov',
                'full_name': 'Орлов Алексей Николаевич',
                'position': 'Специалист технической поддержки',
                'department': departments['IT-отдел'],
                'email': 'orlov@tritochki.local',
                'phone': '+7 900 600-60-60',
                'status': EmployeeProfile.STATUS_WORKS,
                'additional_contact': 'Внутренний номер: 106',
            },
        ]

        for item in profiles_data:
            EmployeeProfile.objects.update_or_create(
                user=users[item['username']],
                defaults={
                    'full_name': item['full_name'],
                    'position': item['position'],
                    'department': item['department'],
                    'email': item['email'],
                    'phone': item['phone'],
                    'status': item['status'],
                    'additional_contact': item['additional_contact'],
                },
            )

    def create_news_categories(self):
        categories = {}
        for name in ['Объявления', 'Компания', 'IT', 'Персонал']:
            category, _ = NewsCategory.objects.get_or_create(name=name)
            categories[name] = category
        return categories

    def create_news(self, categories):
        today = timezone.localdate()
        news_data = [
            {
                'title': 'Запуск корпоративного портала',
                'category': categories['Компания'],
                'content': 'В компании запускается единый портал для сотрудников. Здесь будут новости, документы, справочник и заявки.',
                'publication_date': today,
                'is_important': True,
            },
            {
                'title': 'Обновление правил оформления заявок',
                'category': categories['Объявления'],
                'content': 'Все внутренние обращения теперь можно фиксировать через раздел заявок на портале.',
                'publication_date': today - timedelta(days=1),
                'is_important': True,
            },
            {
                'title': 'Плановые технические работы',
                'category': categories['IT'],
                'content': 'В пятницу вечером возможны кратковременные перерывы в работе внутренних сервисов.',
                'publication_date': today - timedelta(days=2),
                'is_important': False,
            },
            {
                'title': 'Новые материалы в базе знаний',
                'category': categories['Персонал'],
                'content': 'В раздел документов добавлены инструкции по адаптации новых сотрудников.',
                'publication_date': today - timedelta(days=3),
                'is_important': False,
            },
            {
                'title': 'График работы офиса',
                'category': categories['Объявления'],
                'content': 'Административный отдел обновил информацию о графике работы офиса и пропускном режиме.',
                'publication_date': today - timedelta(days=4),
                'is_important': False,
            },
        ]

        for item in news_data:
            News.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )

    def create_document_categories(self):
        categories = {}
        for name in ['Инструкции', 'Регламенты', 'Шаблоны']:
            category, _ = DocumentCategory.objects.get_or_create(name=name)
            categories[name] = category
        return categories

    def create_documents(self, categories):
        documents_data = [
            {
                'title': 'Инструкция по работе с порталом',
                'category': categories['Инструкции'],
                'description': 'Краткое руководство для сотрудников по основным разделам портала.',
                'link': 'https://example.com/portal-guide',
            },
            {
                'title': 'Регламент обработки внутренних заявок',
                'category': categories['Регламенты'],
                'description': 'Описание статусов заявок и порядка их обработки администратором.',
                'link': 'https://example.com/tickets-policy',
            },
            {
                'title': 'Шаблон служебной записки',
                'category': categories['Шаблоны'],
                'description': 'Пример документа для внутренних обращений.',
                'link': 'https://example.com/memo-template',
            },
            {
                'title': 'Правила информационной безопасности',
                'category': categories['Регламенты'],
                'description': 'Базовые правила безопасной работы с корпоративными сервисами.',
                'link': 'https://example.com/security-rules',
            },
            {
                'title': 'Адаптация нового сотрудника',
                'category': categories['Инструкции'],
                'description': 'Памятка для первого рабочего дня и знакомства с внутренними сервисами.',
                'link': 'https://example.com/onboarding',
            },
            {
                'title': 'Шаблон заявки на доступ',
                'category': categories['Шаблоны'],
                'description': 'Пример описания заявки на предоставление доступа.',
                'link': 'https://example.com/access-request',
            },
        ]

        for item in documents_data:
            Document.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )

    def create_service_links(self):
        links_data = [
            {
                'title': 'Корпоративная почта',
                'description': 'Переход к веб-интерфейсу корпоративной почты.',
                'url': 'https://mail.example.com',
                'icon_name': 'Mail',
            },
            {
                'title': 'Облачное хранилище',
                'description': 'Внутренние документы и общие папки компании.',
                'url': 'https://cloud.example.com',
                'icon_name': 'Cloud',
            },
            {
                'title': 'Система учета времени',
                'description': 'Просмотр рабочего времени и отметок посещаемости.',
                'url': 'https://time.example.com',
                'icon_name': 'Time',
            },
            {
                'title': 'База знаний',
                'description': 'Инструкции, регламенты и полезные материалы.',
                'url': 'https://kb.example.com',
                'icon_name': 'KB',
            },
        ]

        for item in links_data:
            CorporateServiceLink.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )

    def create_tickets(self, employee_user):
        tickets_data = [
            {
                'title': 'Не открывается корпоративная почта',
                'description': 'При входе появляется сообщение об ошибке авторизации.',
                'ticket_type': Ticket.TYPE_IT,
                'priority': Ticket.PRIORITY_HIGH,
                'status': Ticket.STATUS_NEW,
                'admin_comment': '',
            },
            {
                'title': 'Нужен доступ к общей папке отдела',
                'description': 'Прошу предоставить доступ к папке с регламентами административного отдела.',
                'ticket_type': Ticket.TYPE_ACCESS,
                'priority': Ticket.PRIORITY_MEDIUM,
                'status': Ticket.STATUS_IN_PROGRESS,
                'admin_comment': 'Заявка передана системному администратору.',
            },
            {
                'title': 'Уточнение по графику отпуска',
                'description': 'Нужно уточнить данные по согласованному отпуску.',
                'ticket_type': Ticket.TYPE_HR,
                'priority': Ticket.PRIORITY_LOW,
                'status': Ticket.STATUS_COMPLETED,
                'admin_comment': 'Информация отправлена сотруднику.',
            },
            {
                'title': 'Замена офисного пропуска',
                'description': 'Старый пропуск поврежден, требуется выпуск нового.',
                'ticket_type': Ticket.TYPE_ADMINISTRATIVE,
                'priority': Ticket.PRIORITY_MEDIUM,
                'status': Ticket.STATUS_IN_PROGRESS,
                'admin_comment': 'Новый пропуск заказан.',
            },
            {
                'title': 'Вопрос по внутреннему документу',
                'description': 'Не могу найти актуальную версию шаблона служебной записки.',
                'ticket_type': Ticket.TYPE_OTHER,
                'priority': Ticket.PRIORITY_LOW,
                'status': Ticket.STATUS_REJECTED,
                'admin_comment': 'Документ уже размещен в разделе "Документы".',
            },
        ]

        for item in tickets_data:
            Ticket.objects.update_or_create(
                author=employee_user,
                title=item['title'],
                defaults=item,
            )
