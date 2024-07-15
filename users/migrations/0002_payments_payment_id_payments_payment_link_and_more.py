# Generated by Django 5.0.6 on 2024-06-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payments",
            name="payment_id",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="id оплаты"
            ),
        ),
        migrations.AddField(
            model_name="payments",
            name="payment_link",
            field=models.CharField(
                blank=True, max_length=400, null=True, verbose_name="ссылка на оплату"
            ),
        ),
        migrations.AddField(
            model_name="payments",
            name="tokens",
            field=models.CharField(
                blank=True, max_length=400, null=True, verbose_name="tokens"
            ),
        ),
    ]