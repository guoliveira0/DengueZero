# Generated by Django 5.2 on 2025-05-08 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_report_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('open', 'Aberto'), ('resolved', 'Resolvido')], default='open', max_length=10, verbose_name='Status'),
        ),
    ]
