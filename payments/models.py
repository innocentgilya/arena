from django.db import models
from userauths.models import User
from django.conf import settings


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # KSh
    max_profiles = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    max_devices = models.PositiveIntegerField(default=1)  # For devices
    duration_days = models.IntegerField(default=30)  # Default duration is 30 days

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # KSh
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)  # Subscription valid until this date

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

