# Generated by Django 4.0.4 on 2022-04-28 06:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Austin', 'Austin'), ('Nashville', 'Nashville'), ('Miami', 'Miami')], max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('date_in', models.DateField()),
                ('date_out', models.DateField()),
                ('numdays', models.PositiveIntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('budget', models.CharField(choices=[('Free', 'Free'), ('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$')], max_length=100)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('capacity', models.CharField(blank=True, max_length=250, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('website', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.city')),
                ('tag', models.ManyToManyField(blank=True, default=None, related_name='event', to='main_app.tag')),
                ('user', models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DayEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveIntegerField()),
                ('event', models.ManyToManyField(to='main_app.event')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.schedule')),
            ],
        ),
    ]
