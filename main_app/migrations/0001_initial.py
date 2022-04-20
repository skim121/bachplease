# Generated by Django 4.0.4 on 2022-04-20 05:34

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('budget', models.CharField(choices=[('Free', 'Free'), ('$', '$'), ('$$', '$$'), ('$$$', '$$$'), ('$$$$', '$$$$')], max_length=100)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('capacity', models.CharField(blank=True, max_length=250, null=True)),
                ('neightborhood', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('website', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.ManyToManyField(default=None, to='main_app.city')),
                ('tag', models.ManyToManyField(blank=True, default=None, related_name='event', to='main_app.tag')),
            ],
        ),
    ]