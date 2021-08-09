# Generated by Django 3.2.5 on 2021-08-09 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210808_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='profile_to_follow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='accounts.profile'),
        ),
    ]