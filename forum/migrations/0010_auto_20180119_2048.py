# Generated by Django 2.0.1 on 2018-01-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20180116_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_processed',
            field=models.TextField(default='', max_length=10000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=10000),
        ),
    ]
