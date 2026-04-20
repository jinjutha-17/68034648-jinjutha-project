$connectionString = "Server=DESKTOP-F51QMJ8\SQLEXPRESS;Database=ApartmentDB;Integrated Security=SSPI;Connection Timeout=30"
$queries = @(
    "IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_TenantSummary') DROP VIEW v_TenantSummary",
    "CREATE VIEW v_TenantSummary AS SELECT t.first_name + ' ' + t.last_name AS Name, r.room_number, b.total_amount FROM tenants_tenant t JOIN rooms_room r ON t.room_id = r.id LEFT JOIN invoices_billing b ON r.id = b.room_id",
    "IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdateRoomStatus') DROP TRIGGER trg_UpdateRoomStatus",
    "CREATE TRIGGER trg_UpdateRoomStatus ON tenants_contract AFTER INSERT AS BEGIN UPDATE r SET r.status = N'ไม่ว่าง' FROM rooms_room r JOIN inserted i ON r.id = i.room_id END"
)

try {
    $connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $connection.Open()
    foreach ($query in $queries) {
        $command = $connection.CreateCommand()
        $command.CommandText = $query
        $command.ExecuteNonQuery() | Out-Null
    }
    $connection.Close()
    Write-Host "SUCCESS: SQL Server Provider confirmed creation of Objects (Views & Triggers)."
} catch {
    Write-Error "DATABASE ERROR: $($_.Exception.Message)"
    exit 1
}
