from django.contrib import admin
from payments.models import SubscriptionPlan, Payment 


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_profiles', 'duration_days']

#from django.contrib import admin
#from payments.models import SubscriptionPlan, Payment

#@admin.register(SubscriptionPlan)
#class SubscriptionPlanAdmin(admin.ModelAdmin):
 #   list_display = ('name', 'price', 'max_profiles')

#@admin.register(Payment)
#class PaymentAdmin(admin.ModelAdmin):
 #   list_display = ('user', 'subscription_plan', 'amount_paid', 'payment_date', 'valid_until')


admin.site.register(SubscriptionPlan, UserAdmin)
admin.site.register(Payment)