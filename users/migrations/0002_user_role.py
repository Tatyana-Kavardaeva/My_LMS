# Generated by Django 4.2.2 on 2024-11-29 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Администратор'), ('teacher', 'Преподаватель'), ('student', 'Студент')], default='student', null=True, verbose_name='Роль'),
        ),
    ]
