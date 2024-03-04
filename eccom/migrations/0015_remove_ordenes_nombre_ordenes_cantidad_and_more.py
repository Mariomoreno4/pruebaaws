# Generated by Django 5.0.1 on 2024-02-24 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eccom', '0014_ordenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenes',
            name='nombre',
        ),
        migrations.AddField(
            model_name='ordenes',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ordenes',
            name='nombre_producto',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ordenes',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='categoria',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='critic_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='platform',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='precio',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='user_score',
            field=models.FloatField(default=0),
        ),
    ]