# Generated by Django 2.2.5 on 2019-09-24 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20190924_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameuser',
            name='rules',
        ),
    ]