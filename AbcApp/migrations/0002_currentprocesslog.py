# Generated by Django 2.2 on 2021-06-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AbcApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentProcessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_id', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
