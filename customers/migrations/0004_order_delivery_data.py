# Generated by Django 5.1.6 on 2025-03-02 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_data',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
