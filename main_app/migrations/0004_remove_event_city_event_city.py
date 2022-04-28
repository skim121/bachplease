# Generated by Django 4.0.4 on 2022-04-26 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_schedule_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='city',
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.city'),
            preserve_default=False,
        ),
    ]