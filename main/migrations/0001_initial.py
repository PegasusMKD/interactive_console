# Generated by Django 2.1.2 on 2019-06-17 06:32

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=175)),
                ('category', models.ManyToManyField(related_name='ingredients', to='main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_of_torture', models.IntegerField()),
                ('index_of_recipe', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                ('ingredient_ammount', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None)),
                ('instructions', models.TextField()),
                ('ingredients', models.ManyToManyField(related_name='recipes', to='main.Ingredient')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lvl_recipes', to='main.Level')),
                ('user', models.ManyToManyField(related_name='user_recipes', to='login.User')),
            ],
        ),
    ]
