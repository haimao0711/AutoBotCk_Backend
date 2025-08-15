from django.db import migrations

def add_acb_stock(apps, schema_editor):
    Stock = apps.get_model('stock', 'Stock')
    Stock.objects.get_or_create(
        symbol='ACB',
        defaults={'name': 'ACB', 'margin': 0}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_stockw1'),  
    ]

    operations = [
        migrations.RunPython(add_acb_stock),
    ]

