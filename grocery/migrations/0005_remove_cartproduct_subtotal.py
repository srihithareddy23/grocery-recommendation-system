# Generated by Django 3.1 on 2021-11-08 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0004_remove_cartproduct_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='subtotal',
        ),
    ]
