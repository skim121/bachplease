# Generated by Django 4.0.4 on 2022-04-28 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayevent',
            name='event',
            field=models.ManyToManyField(related_name='dayevent', to='main_app.event'),
        ),
    ]
