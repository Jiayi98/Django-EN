# Generated by Django 2.2.1 on 2019-07-18 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20190718_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financialcontact',
            old_name='pc_position',
            new_name='fc_position',
        ),
    ]
