# Generated by Django 2.1.10 on 2019-07-20 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookShelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapters', models.TextField(blank=True, null=True)),
                ('books', models.ManyToManyField(to='books.Novel', verbose_name='收藏书本')),
            ],
            options={
                'verbose_name': '书架',
                'verbose_name_plural': '书架',
            },
        ),
    ]
