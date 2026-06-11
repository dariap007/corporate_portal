from django.contrib import admin

from .models import (
    CorporateServiceLink,
    Department,
    Document,
    DocumentCategory,
    EmployeeProfile,
    News,
    NewsCategory,
    Ticket,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'email', 'phone', 'status')
    list_filter = ('department', 'status')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publication_date', 'is_important')
    list_filter = ('category', 'is_important', 'publication_date')
    search_fields = ('title', 'content')


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'link', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')


@admin.register(CorporateServiceLink)
class CorporateServiceLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title', 'description', 'url')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'ticket_type',
        'priority',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('ticket_type', 'priority', 'status', 'created_at')
    search_fields = ('title', 'description', 'author__username', 'admin_comment')
