from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_alter_room_monthly_rent_alter_room_room_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='elec_rate',
            field=models.DecimalField(decimal_places=2, default=7.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='room',
            name='water_rate',
            field=models.DecimalField(decimal_places=2, default=18.0, max_digits=5),
        ),
    ]
