# Generated by Django 2.2.1 on 2019-08-02 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190731_1728'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='myuser',
            table='users_myuser',
        ),
    ]
