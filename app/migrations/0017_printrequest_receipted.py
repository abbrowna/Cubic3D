# Generated by Django 2.1.2 on 2018-11-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_grouprecord_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='printrequest',
            name='receipted',
            field=models.BooleanField(default=False),
        ),
    ]