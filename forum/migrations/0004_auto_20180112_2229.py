# Generated by Django 2.0.1 on 2018-01-12 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20180112_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.TextField(max_length=50, unique=True),
        ),
    ]