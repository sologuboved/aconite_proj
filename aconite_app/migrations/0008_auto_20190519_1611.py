# Generated by Django 2.2.1 on 2019-05-19 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aconite_app', '0007_auto_20190519_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='author',
            new_name='authors',
        ),
    ]
