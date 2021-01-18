# Generated by Django 3.1.5 on 2021-01-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20181120_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='color1',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='material',
            name='color2',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='material',
            name='color3',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='material',
            name='color4',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='material',
            name='color5',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='printrequest',
            name='color',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='quote',
            name='color',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='thingorders',
            name='color',
            field=models.CharField(max_length=15),
        ),
    ]
