# Generated by Django 2.2.1 on 2019-07-24 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20190718_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cfee',
            field=models.FloatField(blank=True, default=0.0, verbose_name='咨费'),
        ),
    ]
