# Generated by Django 5.1 on 2024-09-02 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom', '0005_trending_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Company',
            new_name='Brand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='company',
            new_name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='storage',
            field=models.CharField(default='Unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='trending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Trending',
        ),
    ]