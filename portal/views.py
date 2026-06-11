from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .models import CorporateServiceLink, Document, News, Ticket


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
