# Generated by Django 2.2 on 2021-06-24 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AbcApp', '0006_auto_20210624_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentprocesslog',
            name='process_status',
            field=models.CharField(default='Stopped', max_length=500, null=True),
        ),
    ]
