# Generated by Django 5.0.3 on 2024-05-04 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_image_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tiki_product_id',
            field=models.IntegerField(default=0),
        ),
    ]
