from django.db import migrations, models
import django.db.models.deletion


def create_tenant_summary_view(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        return
    schema_editor.execute("DROP VIEW IF EXISTS v_TenantSummary;")
    schema_editor.execute(
        """
        CREATE VIEW v_TenantSummary AS
        SELECT
            t.id AS TenantID,
            t.first_name || ' ' || t.last_name AS FullName,
            r.room_number AS RoomNumber,
            (
                SELECT b.total_amount
                FROM invoices_billing b
                WHERE b.room_id = r.id
                ORDER BY b.service_month DESC
                LIMIT 1
            ) AS LatestInvoiceAmount,
            (
                SELECT COUNT(*)
                FROM parcels_parcel p
                WHERE p.tenant_id = t.id AND p.status = 'pending'
            ) AS PendingParcels
        FROM tenants_tenant t
        LEFT JOIN rooms_room r ON t.room_id = r.id;
        """
    )


def drop_tenant_summary_view(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        return
    schema_editor.execute("DROP VIEW IF EXISTS v_TenantSummary;")


def create_update_room_status_trigger(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        return
    schema_editor.execute("DROP TRIGGER IF EXISTS trg_UpdateRoomStatus;")
    schema_editor.execute(
        """
        CREATE TRIGGER trg_UpdateRoomStatus
        AFTER INSERT ON tenants_contract
        FOR EACH ROW
        BEGIN
            UPDATE rooms_room
            SET status = 'ไม่ว่าง'
            WHERE id = NEW.room_id;
        END;
        """
    )


def drop_update_room_status_trigger(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        return
    schema_editor.execute("DROP TRIGGER IF EXISTS trg_UpdateRoomStatus;")


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0003_employeepermission'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        # 1. Update UserProfile roles (Client -> Tenant)
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Staff', 'Staff'), ('Tenant', 'Tenant')], default='Tenant', max_length=20),
        ),
        # 2. Add Contract Model
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_date', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='rooms.room')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='tenants.tenant')),
            ],
        ),
        # 3. Create SQL View v_TenantSummary (Moved to manual deployment to avoid circular dependency)
        # migrations.RunPython(create_tenant_summary_view, drop_tenant_summary_view),
        # 4. Create SQL Trigger trg_UpdateRoomStatus (Moved to manual deployment)
        # migrations.RunPython(create_update_room_status_trigger, drop_update_room_status_trigger),
    ]
