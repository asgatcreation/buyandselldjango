# Generated by Django 4.0 on 2022-11-23 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_number',
            field=models.CharField(default='00000000000', max_length=100),
        ),
    ]
