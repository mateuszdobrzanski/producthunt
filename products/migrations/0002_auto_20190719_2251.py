# Generated by Django 2.2 on 2019-07-19 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pub_type',
            new_name='pub_date',
        ),
    ]
