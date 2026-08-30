param(
  [int]$Port = 8080
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "NCUT AI Local CMS security check" -ForegroundColor Cyan

try {
  $defender = Get-MpComputerStatus
  Write-Host "Microsoft Defender Antivirus enabled: $($defender.AMServiceEnabled)"
  Write-Host "Real-time protection enabled: $($defender.RealTimeProtectionEnabled)"
} catch {
  Write-Warning "Unable to read Microsoft Defender status. Open Windows Security to confirm protection is enabled."
}

try {
  Get-NetFirewallProfile | ForEach-Object {
    Write-Host "Windows Defender Firewall $($_.Name): Enabled=$($_.Enabled)"
  }
} catch {
  Write-Warning "Unable to read Windows Firewall status."
}

if (-not $env:NCUT_ADMIN_PASSWORD) {
  Write-Warning "NCUT_ADMIN_PASSWORD is not set. Set a strong password before regular use."
  Write-Host 'Example: $env:NCUT_ADMIN_PASSWORD="your-strong-password"'
}

$env:HOST = "127.0.0.1"
$env:PORT = [string]$Port

Set-Location $projectRoot
Write-Host "Starting local-only CMS at http://127.0.0.1:$Port/admin/" -ForegroundColor Green
python server.py
