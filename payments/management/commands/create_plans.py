from django.core.management.base import BaseCommand
from payments.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Create subscription plans'

    def handle(self, *args, **options):
        # Define your plans
        plans = [
            {'name': 'Basic Plan', 'price': 350, 'description': '1 Profile, All Available PastPapers, All Available Textbooks, All Available Books'},
            {'name': 'Intermediate Plan', 'price': 550, 'description': '2 Profiles, All Available PastPapers, All Available Textbooks, All Available Books'},
            {'name': 'Premium Plan', 'price': 900, 'description': '4 Profiles, All Available PastPapers, All Available Textbooks, All Available Books'},
        ]

        # Create the plans in the database
        for plan in plans:
            SubscriptionPlan.objects.update_or_create(
                name=plan['name'], 
                defaults={'price': plan['price'], 'description': plan['description']}
            )
        self.stdout.write(self.style.SUCCESS('Subscription plans created successfully!'))
