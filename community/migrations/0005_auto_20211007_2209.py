# Generated by Django 3.2.5 on 2021-10-07 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0004_responses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responses',
            name='community',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='community.community'),
        ),
        migrations.AlterField(
            model_name='responses',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
