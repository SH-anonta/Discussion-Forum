# Generated by Django 2.0.1 on 2018-01-19 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20180119_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='processed',
            new_name='content_processed',
        ),
    ]