# Generated by Django 4.1.7 on 2023-05-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_biglimitsez'),
    ]

    operations = [
        migrations.AddField(
            model_name='biglimitsez',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
