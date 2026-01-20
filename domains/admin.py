from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Domain, Notification, CheckLog


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в списке
    list_display = ('name', 'user', 'expiration_date', 'days_left', 'registrar', 'created_at')

    # Фильтры справа
    list_filter = ('expiration_date', 'registrar', 'user')

    # Поиск по полям
    search_fields = ('name', 'user__username', 'registrar')

    # Сортировка по умолчанию
    ordering = ('days_left',)

    # Разбивка на страницы
    list_per_page = 20

    # Поля только для чтения при редактировании
    readonly_fields = ('created_at', 'updated_at', 'days_left')

    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'name', 'expiration_date', 'days_left')
        }),
        ('Дополнительно', {
            'fields': ('registrar', 'created_at', 'updated_at')
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('domain', 'notification_type', 'status', 'scheduled_for', 'sent_at')
    list_filter = ('status', 'notification_type', 'scheduled_for')
    search_fields = ('domain__name',)
    readonly_fields = ('created_at',)
    list_per_page = 20


@admin.register(CheckLog)
class CheckLogAdmin(admin.ModelAdmin):
    list_display = ('domain', 'checked_at', 'expiration_date', 'registrar', 'success')
    list_filter = ('success', 'checked_at')
    search_fields = ('domain__name', 'registrar')
    readonly_fields = ('checked_at',)
    list_per_page = 20