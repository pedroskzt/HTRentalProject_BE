# Generated by Django 4.2.13 on 2024-06-18 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tools',
            name='image_name',
            field=models.TextField(null=True),
        ),
    ]