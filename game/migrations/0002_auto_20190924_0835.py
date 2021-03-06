# Generated by Django 2.2.5 on 2019-09-24 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='user',
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='game.GameUser')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='option',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='game.Option'),
            preserve_default=False,
        ),
    ]
