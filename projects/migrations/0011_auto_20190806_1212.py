# Generated by Django 2.2.1 on 2019-08-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20190802_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project2expert',
            name='fee_index',
            field=models.FloatField(blank=True, default=1.0, verbose_name='咨费系数'),
        ),
    ]