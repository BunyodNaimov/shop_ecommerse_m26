# Generated by Django 5.0.6 on 2024-06-10 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_productattribute_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productattribute',
            unique_together=set(),
        ),
    ]
