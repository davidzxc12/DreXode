# Generated by Django 2.0.1 on 2018-01-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='userID',
            field=models.CharField(max_length=100),
        ),
    ]