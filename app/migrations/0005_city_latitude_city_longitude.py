# Generated by Django 4.2.4 on 2023-09-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_night_life'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
