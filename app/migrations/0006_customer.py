# Generated by Django 4.2.4 on 2023-08-13 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_category_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
    ]
