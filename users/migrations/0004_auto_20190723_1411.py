# Generated by Django 2.2.1 on 2019-07-23 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190708_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'permissions': (('can_view_contact_info', '查看联系方式'), ('can_view_pm_contact_info', '查看项目经理联系方式'))},
        ),
    ]