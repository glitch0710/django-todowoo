# Generated by Django 3.2.5 on 2021-12-31 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='important',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]