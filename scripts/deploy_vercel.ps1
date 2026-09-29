param (
    [string]$ProjectPath = "projects/micro_saas/synapse_geo",
    [switch]$Prod
)

$envFile = Join-Path $PSScriptRoot "..\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "[!] File .env không tồn tại. Vui lòng tạo file .env từ .env.example." -ForegroundColor Red
    exit 1
}

# Đọc file .env
$envLines = Get-Content $envFile
$token = ""
foreach ($line in $envLines) {
    if ($line -match "^\s*VERCEL_TOKEN\s*=\s*(.+)$") {
        $token = $matches[1].Trim().Trim('"').Trim("'")
    }
}

if (-not $token) {
    Write-Host "[!] VERCEL_TOKEN chưa được điền trong file .env." -ForegroundColor Yellow
    Write-Host "    Vui lòng mở file .env và điền: VERCEL_TOKEN=your_token_here" -ForegroundColor Yellow
    exit 1
}

$fullTarget = Join-Path $PSScriptRoot "..\$ProjectPath"
if (-not (Test-Path $fullTarget)) {
    Write-Host "[!] Thư mục dự án không tồn tại: $fullTarget" -ForegroundColor Red
    exit 1
}

Write-Host "=== Bắt đầu deploy [$ProjectPath] lên Vercel ===" -ForegroundColor Cyan
$cmdArgs = @("--yes", "vercel", $fullTarget, "--token", $token)
if ($Prod) {
    $cmdArgs += "--prod"
}

npx @cmdArgs
