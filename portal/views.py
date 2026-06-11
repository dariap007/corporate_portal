from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CorporateServiceLinkAdminForm,
    DepartmentAdminForm,
    DocumentAdminForm,
    EmployeeAdminForm,
    EmployeeCreateForm,
    NewsAdminForm,
    ProfileEditForm,
    TicketAdminForm,
    TicketForm,
)
from .models import CorporateServiceLink, Department, Document, EmployeeProfile, News, Ticket


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url='home')(view_func)


def filter_by_casefold(queryset, field_name, search_query):
    normalized_query = search_query.casefold()
    matching_ids = [
        item.id
        for item in queryset
        if normalized_query in (getattr(item, field_name) or '').casefold()
    ]
    return queryset.filter(id__in=matching_ids)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get('next') or 'home'
        return redirect(next_url)

    return render(request, 'portal/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    active_statuses = [Ticket.STATUS_NEW, Ticket.STATUS_IN_PROGRESS]
    if request.user.is_staff:
        tickets = Ticket.objects.select_related('author').all()
        active_tickets_title = 'Активные заявки сотрудников'
    else:
        tickets = Ticket.objects.filter(author=request.user).select_related('author')
        active_tickets_title = 'Активные заявки'

    active_tickets = tickets.filter(status__in=active_statuses)

    context = {
        'latest_news': News.objects.select_related('category')[:3],
        'service_links': CorporateServiceLink.objects.all()[:4],
        'active_tickets': active_tickets[:5],
        'active_tickets_title': active_tickets_title,
        'news_count': News.objects.count(),
        'documents_count': Document.objects.count(),
        'active_tickets_count': active_tickets.count(),
    }
    return render(request, 'portal/home.html', context)


@login_required
def news_list_view(request):
    news_list = News.objects.select_related('category').all()
    return render(request, 'portal/news_list.html', {'news_list': news_list})


@login_required
def news_detail_view(request, news_id):
    news = get_object_or_404(News.objects.select_related('category'), id=news_id)
    return render(request, 'portal/news_detail.html', {'news': news})


@login_required
def employees_list_view(request):
    search_query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '').strip()

    employees = EmployeeProfile.objects.select_related('department', 'user').all()
    departments = Department.objects.all()

    if department_id:
        employees = employees.filter(department_id=department_id)

    if search_query:
        employees = filter_by_casefold(employees, 'full_name', search_query)

    context = {
        'employees': employees,
        'departments': departments,
        'search_query': search_query,
        'selected_department': department_id,
    }
    return render(request, 'portal/employees_list.html', context)


@login_required
def employee_detail_view(request, employee_id):
    employee = get_object_or_404(
        EmployeeProfile.objects.select_related('department', 'user'),
        id=employee_id,
    )
    return render(request, 'portal/employee_detail.html', {'employee': employee})


@login_required
def documents_list_view(request):
    search_query = request.GET.get('q', '').strip()
    documents = Document.objects.select_related('category').all()

    if search_query:
        documents = filter_by_casefold(documents, 'title', search_query)

    context = {
        'documents': documents,
        'search_query': search_query,
    }
    return render(request, 'portal/documents_list.html', context)


@login_required
def tickets_list_view(request):
    if request.user.is_staff:
        tickets = Ticket.objects.select_related('author').all()
        page_title = 'Все заявки'
        page_description = 'Администратор видит заявки всех сотрудников. Статус и комментарий можно изменить через раздел управления.'
    else:
        tickets = Ticket.objects.filter(author=request.user).select_related('author')
        page_title = 'Мои заявки'
        page_description = 'Здесь отображаются только заявки, созданные текущим пользователем.'

    context = {
        'tickets': tickets,
        'page_title': page_title,
        'page_description': page_description,
    }
    return render(request, 'portal/tickets_list.html', context)


@login_required
def ticket_create_view(request):
    form = TicketForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.author = request.user
        ticket.status = Ticket.STATUS_NEW
        ticket.save()
        return redirect('tickets_list')

    return render(request, 'portal/ticket_create.html', {'form': form})


@login_required
def profile_view(request):
    profile = get_object_or_404(
        EmployeeProfile.objects.select_related('department', 'user'),
        user=request.user,
    )
    latest_tickets = Ticket.objects.filter(author=request.user)[:5]
    role_name = 'Администратор' if request.user.is_staff or request.user.is_superuser else 'Сотрудник'

    context = {
        'profile': profile,
        'latest_tickets': latest_tickets,
        'role_name': role_name,
    }
    return render(request, 'portal/profile.html', context)


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    form = ProfileEditForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'portal/profile_edit.html', {'form': form, 'profile': profile})


@login_required
@staff_required
def management_dashboard_view(request):
    return redirect('home')


@login_required
@staff_required
def management_news_list_view(request):
    return redirect('news_list')


@login_required
@staff_required
def management_news_create_view(request):
    form = NewsAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Новость создана.')
        return redirect('news_list')
    return render(request, 'portal/management/news_form.html', {'form': form, 'page_title': 'Создание новости'})


@login_required
@staff_required
def management_news_edit_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    form = NewsAdminForm(request.POST or None, instance=news)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Новость обновлена.')
        return redirect('news_list')
    return render(request, 'portal/management/news_form.html', {'form': form, 'page_title': 'Редактирование новости'})


@login_required
@staff_required
def management_news_delete_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена.')
        return redirect('news_list')
    return render(request, 'portal/management/confirm_delete.html', {
        'object_name': news.title,
        'cancel_url': 'news_list',
        'page_title': 'Удаление новости',
    })


@login_required
@staff_required
def management_employees_list_view(request):
    return redirect('employees_list')


@login_required
@staff_required
def management_employee_create_view(request):
    form = EmployeeCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Сотрудник создан.')
        return redirect('employees_list')
    return render(request, 'portal/management/employee_form.html', {'form': form, 'page_title': 'Создание сотрудника'})


@login_required
@staff_required
def management_employee_edit_view(request, employee_id):
    employee = get_object_or_404(EmployeeProfile.objects.select_related('user'), id=employee_id)
    form = EmployeeAdminForm(request.POST or None, instance=employee)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Сотрудник обновлён.')
        return redirect('employees_list')
    return render(request, 'portal/management/employee_form.html', {'form': form, 'page_title': 'Редактирование сотрудника'})


@login_required
@staff_required
def management_employee_delete_view(request, employee_id):
    employee = get_object_or_404(EmployeeProfile.objects.select_related('user'), id=employee_id)
    if employee.user == request.user:
        messages.error(request, 'Нельзя удалить собственную учётную запись.')
        return redirect('employees_list')
    if request.method == 'POST':
        employee.user.delete()
        messages.success(request, 'Сотрудник удалён.')
        return redirect('employees_list')
    return render(request, 'portal/management/confirm_delete.html', {
        'object_name': employee.full_name,
        'cancel_url': 'employees_list',
        'page_title': 'Удаление сотрудника',
    })


@login_required
@staff_required
def management_documents_list_view(request):
    return redirect('documents_list')


@login_required
@staff_required
def management_document_create_view(request):
    form = DocumentAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Документ создан.')
        return redirect('documents_list')
    return render(request, 'portal/management/document_form.html', {'form': form, 'page_title': 'Создание документа'})


@login_required
@staff_required
def management_document_edit_view(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    form = DocumentAdminForm(request.POST or None, instance=document)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Документ обновлён.')
        return redirect('documents_list')
    return render(request, 'portal/management/document_form.html', {'form': form, 'page_title': 'Редактирование документа'})


@login_required
@staff_required
def management_document_delete_view(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Документ удалён.')
        return redirect('documents_list')
    return render(request, 'portal/management/confirm_delete.html', {
        'object_name': document.title,
        'cancel_url': 'documents_list',
        'page_title': 'Удаление документа',
    })


@login_required
@staff_required
def management_tickets_list_view(request):
    return redirect('tickets_list')


@login_required
@staff_required
def management_ticket_edit_view(request, ticket_id):
    ticket = get_object_or_404(Ticket.objects.select_related('author'), id=ticket_id)
    form = TicketAdminForm(request.POST or None, instance=ticket)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Заявка обновлена.')
        return redirect('tickets_list')
    return render(request, 'portal/management/ticket_form.html', {'form': form, 'ticket': ticket})


@login_required
@staff_required
def management_departments_list_view(request):
    departments = Department.objects.all()
    return render(request, 'portal/management/departments_list.html', {'departments': departments})


@login_required
@staff_required
def management_department_create_view(request):
    form = DepartmentAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Подразделение создано.')
        return redirect('management_departments_list')
    return render(request, 'portal/management/department_form.html', {'form': form, 'page_title': 'Создание подразделения'})


@login_required
@staff_required
def management_department_edit_view(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    form = DepartmentAdminForm(request.POST or None, instance=department)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Подразделение обновлено.')
        return redirect('management_departments_list')
    return render(request, 'portal/management/department_form.html', {'form': form, 'page_title': 'Редактирование подразделения'})


@login_required
@staff_required
def management_department_delete_view(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Подразделение удалено.')
        return redirect('management_departments_list')
    return render(request, 'portal/management/confirm_delete.html', {
        'object_name': department.name,
        'cancel_url': 'management_departments_list',
        'page_title': 'Удаление подразделения',
    })


@login_required
@staff_required
def management_service_links_list_view(request):
    service_links = CorporateServiceLink.objects.all()
    return render(request, 'portal/management/service_links_list.html', {'service_links': service_links})


@login_required
@staff_required
def management_service_link_create_view(request):
    form = CorporateServiceLinkAdminForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ссылка на сервис создана.')
        return redirect('management_service_links_list')
    return render(request, 'portal/management/service_link_form.html', {'form': form, 'page_title': 'Создание ссылки на сервис'})


@login_required
@staff_required
def management_service_link_edit_view(request, service_link_id):
    service_link = get_object_or_404(CorporateServiceLink, id=service_link_id)
    form = CorporateServiceLinkAdminForm(request.POST or None, instance=service_link)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ссылка на сервис обновлена.')
        return redirect('management_service_links_list')
    return render(request, 'portal/management/service_link_form.html', {'form': form, 'page_title': 'Редактирование ссылки на сервис'})


@login_required
@staff_required
def management_service_link_delete_view(request, service_link_id):
    service_link = get_object_or_404(CorporateServiceLink, id=service_link_id)
    if request.method == 'POST':
        service_link.delete()
        messages.success(request, 'Ссылка на сервис удалена.')
        return redirect('management_service_links_list')
    return render(request, 'portal/management/confirm_delete.html', {
        'object_name': service_link.title,
        'cancel_url': 'management_service_links_list',
        'page_title': 'Удаление ссылки на сервис',
    })
