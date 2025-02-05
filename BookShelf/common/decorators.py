from functools import wraps
from django.http import JsonResponse
from django.utils.timezone import now
from payments.models import Payment
from user_sessions.models import Session

def subscription_required(view_func):
    '''Restricting Profile Access Based on Plan and Active Device Limit'''
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # Ensure user is authenticated
        if not user.is_authenticated:
            return JsonResponse({'error': 'Login required to access this resource.'}, status=401)

        # Check for an active subscription payment
        active_payment = Payment.objects.filter(user=user).order_by('-created_at').first()
        if not active_payment:
            return JsonResponse({'error': 'Subscription required to access this resource.'}, status=403)

        # Check subscription validity
        if active_payment.valid_until < now().date():
            return JsonResponse({'error': 'Subscription expired. Please renew your plan.'}, status=403)

        # Enforce active device limit based on subscription plan
        max_devices = active_payment.plan.max_devices  # Assume the plan has a 'max_devices' field
        active_sessions = Session.objects.filter(user=user)

        if active_sessions.count() > max_devices:
            return JsonResponse({
                'error': 'You have exceeded the maximum number of active devices allowed by your subscription plan.'
            }, status=403)

        # All checks passed, allow access
        return view_func(request, *args, **kwargs)

    return _wrapped_view


