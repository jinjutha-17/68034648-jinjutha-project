# PostgreSQL Unlock & Reset Script (LuxeDorm Edition)
# Run as Administrator to bypass password authentication and set it to '1234'

$pgPath = "C:\Program Files\PostgreSQL\17"
$psql = "$pgPath\bin\psql.exe"
$pgData = "$pgPath\data"
$hbaFile = "$pgData\pg_hba.conf"

Write-Host "--- PostgreSQL Unlock System ---" -ForegroundColor Cyan

if (-not (Test-Path $psql)) {
    Write-Error "PostgreSQL 17 psql.exe not found at $psql"
    exit 1
}

# 1. Temporarily backup and modify pg_hba.conf to 'trust'
Write-Host "Step 1: Unlocking authentication door (pg_hba.conf)..."
if (Test-Path $hbaFile) {
    Copy-Item $hbaFile "$hbaFile.bak" -Force
    # Replace scram-sha-256 or md5 with trust for localhost
    (Get-Content $hbaFile) -replace 'scram-sha-256|md5', 'trust' | Set-Content $hbaFile -Force
    Write-Host "Authentication set to TRUST temporarily." -ForegroundColor Green
} else {
    Write-Warning "Could not find pg_hba.conf at $hbaFile. This script may need to be run as Administrator."
}

# 2. Restart the service to apply 'trust'
Write-Host "Step 2: Restarting PostgreSQL service..."
Restart-Service postgresql* -ErrorAction SilentlyContinue

# 3. Reset the password for user 'postgres'
Write-Host "Step 3: Resetting 'postgres' password to '1234'..."
Start-Sleep -Seconds 2
& $psql -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD '1234';" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Password for 'postgres' has been reset to '1234'." -ForegroundColor Green
} else {
    Write-Error "Failed to reset password. Ensure the service is running and you have enough permissions."
}

# 4. Restore original security settings
Write-Host "Step 4: Restoring security settings..."
if (Test-Path "$hbaFile.bak") {
    Move-Item "$hbaFile.bak" $hbaFile -Force
    Write-Host "pg_hba.conf restored from backup."
}

# 5. Final Restart
Write-Host "Step 5: Final service restart..."
Restart-Service postgresql* -ErrorAction SilentlyContinue

Write-Host "--- UNLOCK COMPLETE ---" -ForegroundColor Cyan
Write-Host "You can now connect to PostgreSQL with password '1234'."
