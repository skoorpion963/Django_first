# Generated by Django 4.1.7 on 2023-05-19 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_alter_biglimits_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSubId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatId', models.IntegerField()),
                ('timeEndSub', models.DateTimeField()),
            ],
        ),
    ]