# Generated by Django 4.2.13 on 2024-07-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_history_chatbotuserhistory_chat_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbotuserhistory',
            name='chat_history',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
