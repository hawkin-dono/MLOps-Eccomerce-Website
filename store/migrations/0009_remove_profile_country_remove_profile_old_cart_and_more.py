# Generated by Django 5.0.3 on 2024-05-07 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_brand_id_product_brand_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='old_cart',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='zipcode',
        ),
    ]