# Generated by Django 2.2.1 on 2019-05-22 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aconite_app', '0009_auto_20190519_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='dedication',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='dedication',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='year_demo',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='original_title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]