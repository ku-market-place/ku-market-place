from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "ku_market_place",
            "0003_remove_product_category_id_alter_customer_email_and_more",
        ),
        ('ku_market_place', '0003_remove_product_category_id_alter_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
