# Generated by Django 2.2.2 on 2019-06-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='looked_up',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='recognized',
            field=models.CharField(default='', max_length=30),
        ),
    ]
