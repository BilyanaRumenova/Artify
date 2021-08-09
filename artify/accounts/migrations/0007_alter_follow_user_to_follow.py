# Generated by Django 3.2.5 on 2021-08-05 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_following_user_id_follow_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='user_to_follow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='accounts.profile'),
        ),
    ]