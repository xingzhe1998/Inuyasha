# Generated by Django 2.1.10 on 2019-07-22 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_flash_generalize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heat',
            name='read_num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
