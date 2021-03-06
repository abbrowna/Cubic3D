# Generated by Django 3.1.6 on 2021-05-08 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Filament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diameter', models.DecimalField(choices=[(1.75, '1.75'), (2.85, '2.85')], decimal_places=2, max_digits=3)),
                ('stock', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
                ('net_weight', models.IntegerField(choices=[(250, '250g'), (500, '500g'), (750, '750g'), (1000, '1Kg')])),
                ('price', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('characteristics', models.TextField(blank=True)),
                ('print_temp', models.CharField(blank=True, max_length=15)),
                ('bed_temp', models.CharField(blank=True, max_length=15)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=100)),
                ('phone', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('item_total', models.IntegerField(default=0)),
                ('delivery_fee', models.IntegerField(default=350)),
                ('alt_name', models.CharField(blank=True, max_length=50)),
                ('alt_phone', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('filament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.filament')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='region',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.region'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='filament',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.material'),
        ),
    ]
