# Generated by Django 5.0.6 on 2024-07-24 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_initial'),
        ('userauths', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_book', to='userauths.profile'),
        ),
    ]
