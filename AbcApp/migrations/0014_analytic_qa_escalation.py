# Generated by Django 2.2 on 2021-07-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AbcApp', '0013_analytic_currentprocesslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='qa_escalation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
