from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Domain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='domains')
    name = models.CharField(max_length=255, verbose_name="Доменное имя")
    expiration_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)
    registrar = models.CharField(max_length=255, verbose_name="Регистратор", blank=True)
    days_left = models.IntegerField(verbose_name="Дней до окончания", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['days_left']

    def __str__(self):
        return self.name

    def update_days_left(self):
        if self.expiration_date:
            self.days_left = (self.expiration_date - timezone.now().date()).days
            self.save()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('telegram', 'Telegram'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='email')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    scheduled_for = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain.name} - {self.get_status_display()}"


class CheckLog(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='check_logs')
    checked_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    registrar = models.CharField(max_length=255)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.domain.name} - {self.checked_at}"