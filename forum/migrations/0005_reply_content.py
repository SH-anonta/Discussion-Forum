# Generated by Django 2.0.1 on 2018-01-12 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20180112_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='content',
            field=models.TextField(default='a', max_length=16),
            preserve_default=False,
        ),
    ]
