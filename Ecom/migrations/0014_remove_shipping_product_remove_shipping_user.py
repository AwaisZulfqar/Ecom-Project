# Generated by Django 5.1 on 2024-09-05 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0013_alter_shipping_area_code_alter_shipping_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='product',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='user',
        ),
    ]
