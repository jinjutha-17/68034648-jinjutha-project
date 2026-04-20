from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meter',
            name='water_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='meter',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
