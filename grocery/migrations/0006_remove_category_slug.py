# Generated by Django 3.1 on 2021-11-08 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0005_remove_cartproduct_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
