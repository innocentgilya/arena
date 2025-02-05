import random
import string
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from payments.models import SubscriptionPlan, Payment
from userauths.models import Profile
from django.http import JsonResponse
import requests
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import uuid
from decimal import Decimal






from django.urls import reverse





@login_required
def select_plan(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan")
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        reference = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        return redirect(reverse('payments:create_payment', kwargs={'plan_id': plan.id, 'reference': reference}))
    plans = SubscriptionPlan.objects.all()
    return render(request, "payment/subscription_plans.html", {"plans": plans})





@login_required
def create_payment(request, plan_id, reference):
    try:
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        valid_until_date = timezone.now() + timedelta(days=plan.duration_days)

        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            reference=reference,
            valid_until=valid_until_date,
        )
    
        return JsonResponse({"success": True, "message": "Payment record created successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Failed to create payment record: {e}"}, status=500)




def initialize_paystack_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": request.user.email,
        "amount": int(payment.amount * 100),  # Amount in kobo
        "reference": reference,
        "callback_url": f"{settings.BASE_URL}/payment/verify/{reference}/",
    }

    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()

    if response.status_code == 200 and res_data["status"]:
        return redirect(res_data["data"]["authorization_url"])

    return JsonResponse({"success": False, "message": "Payment initialization failed"}, status=500)





#########################
######################
####################


@csrf_exempt
def validate_reference(request):
    '''This view validates the presence of a reference in the request.'''
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reference = data.get("reference")

            if not reference:
                return JsonResponse({"error": "Reference is required"}, status=400)

            return JsonResponse({"success": True, "reference": reference})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def verify_with_paystack(request):
    '''This view handles the API call to Paystack to verify the payment.'''
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reference = data.get("reference")

            if not reference:
                return JsonResponse({"error": "Reference is required"}, status=400)

            url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            res_data = response.json()

            if response.status_code == 200 and res_data["status"] and res_data["data"]["status"] == "success":
                return JsonResponse({"success": True, "paystack_data": res_data})
            else:
                return JsonResponse({"error": "Payment verification failed"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# '''This view handles the database update after verifying the payment.'''

import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reference = data.get("reference")

            if not reference:
                logger.error("Reference is required but missing.")
                return JsonResponse({"error": "Reference is required"}, status=400)

            # Check the payment record
            try:
                payment = Payment.objects.get(reference=reference)
                payment.verified = True
                payment.save()

                # Ensure user profile creation
                user = payment.user
                profile, created = Profile.objects.get_or_create(user=user)
                if created:
                    logger.info(f"Profile created for user: {user.username}")

                # Update the user's subscription (assuming max_profiles is a field in the Profile model)
                profile.max_profiles = payment.plan.max_profiles
                profile.save()

                # Redirect to profile create page after successful payment
                return JsonResponse({
                    "success": True,
                    "redirect_url": reverse("userauths:profile-create")
                })

            except Payment.DoesNotExist:
                logger.error(f"Payment record not found for reference: {reference}")
                return JsonResponse({"error": "Payment record not found"}, status=404)

        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)












@login_required
def subscription_plans_view(request):
    '''a view to describe the subscription page and how it will work.'''
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans': plans
    }
    return render(request, 'payment/subscription_plans.html', context)


