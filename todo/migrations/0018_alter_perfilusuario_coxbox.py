# Generated by Django 5.0.1 on 2024-03-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eccom', '0017_perfilusuario_imagen_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='coxbox',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]