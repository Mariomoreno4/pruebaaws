# Generated by Django 5.0.1 on 2024-02-21 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eccom', '0008_producto_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='favoritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('pic', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
