# Generated by Django 3.2.5 on 2021-08-05 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_delete_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.profile')),
            ],
        ),
    ]