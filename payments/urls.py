from django.urls import path
from payments import views

app_name = "payments"

urlpatterns = [


    #path("payment/initialize/", views.initialize_payment, name="initialize_payment"),


    #path('payment/verify/', views.verify_payment, name='verify_payment'),


    path("select-plans/", views.select_plan, name="select_plan"),


    path("payment/create/<int:plan_id>/<str:reference>/", views.create_payment, name="create_payment"),


    path("payment/initialize/<str:reference>/", views.initialize_paystack_payment, name="initialize_paystack_payment"),


    path('subscription-plans/', views.subscription_plans_view, name='subscription_plans'),


    path("payment/validate-reference/", views.validate_reference, name="validate_reference"),


    path("payment/verify-with-paystack/", views.verify_with_paystack, name="verify_with_paystack"),


    path("payment/process-payment/", views.process_payment, name="process_payment")

]


