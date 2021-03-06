# Generated by Django 2.1.2 on 2018-11-02 19:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_material_ppg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='color',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='quote',
            name='material',
            field=models.ForeignKey(default='PLA', on_delete=django.db.models.deletion.CASCADE, to='app.Material'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='thing',
            field=models.FileField(upload_to='thingstemp/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(['stl'], 'Please upload your file as a .STL Most CAD software are capable of exporting models in this format.')]),
        ),
    ]
