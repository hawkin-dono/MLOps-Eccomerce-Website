# Generated by Django 5.0.3 on 2024-05-09 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_tiki_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tiki_product_id',
        ),
    ]
