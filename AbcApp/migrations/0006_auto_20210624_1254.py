# Generated by Django 2.2 on 2021-06-24 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AbcApp', '0005_analytic_currentprocesslog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currentprocesslog',
            old_name='process_id',
            new_name='process_status',
        ),
    ]
