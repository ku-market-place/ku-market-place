# Generated by Django 4.2.4 on 2023-10-31 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=200)),
                ("category_description", models.CharField(max_length=200)),
                ("category_image", models.CharField(max_length=200)),
                ("category_parent_id", models.IntegerField(default=0)),
                ("category_status", models.IntegerField(default=0)),
                (
                    "category_date_added",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date added"
                    ),
                ),
                (
                    "category_date_modified",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date modified"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=200)),
                ("lastname", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200)),
                ("address", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=200)),
                ("balance", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("total_amount", models.IntegerField(default=0)),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ku_market_place.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shipping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ku_market_place.customer",
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ku_market_place.order",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=200)),
                ("price", models.IntegerField(default=0)),
                ("quantity", models.IntegerField(default=0)),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ku_market_place.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=0)),
                ("subtotal", models.IntegerField(default=0)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ku_market_place.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="order_item_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ku_market_place.orderitem",
            ),
        ),
    ]
