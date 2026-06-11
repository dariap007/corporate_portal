from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import CorporateServiceLink, Department, Document, EmployeeProfile, News, Ticket


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
    user_tickets = Ticket.objects.filter(author=request.user)

    context = {
        'latest_news': News.objects.select_related('category')[:3],
        'service_links': CorporateServiceLink.objects.all()[:4],
        'active_tickets': user_tickets.filter(status__in=active_statuses)[:5],
        'news_count': News.objects.count(),
        'documents_count': Document.objects.count(),
        'active_tickets_count': user_tickets.filter(status__in=active_statuses).count(),
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

    if search_query:
        employees = employees.filter(full_name__icontains=search_query)

    if department_id:
        employees = employees.filter(department_id=department_id)

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
