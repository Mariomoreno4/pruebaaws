# Generated by Django 5.0.1 on 2024-02-24 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eccom', '0013_perfilusuario_genero'),
    ]

    operations = [
        migrations.CreateModel(
            name='ordenes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('critic_score', models.FloatField()),
                ('user_score', models.FloatField()),
            ],
        ),
    ]
