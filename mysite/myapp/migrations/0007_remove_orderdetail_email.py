# Generated by Django 3.2.16 on 2022-11-29 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_orderdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='email',
        ),
    ]
