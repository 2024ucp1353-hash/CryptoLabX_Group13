# ==============================================================================
# Cryptography Laboratory - OS Random Number Generation
# Windows CNG / .NET RandomNumberGenerator 1 MiB Data Generation Script
# ==============================================================================

# Ensure output directory exists
$outputDir = Join-Path -Path $PSScriptRoot -ChildPath "data"
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$outputFile = Join-Path -Path $outputDir -ChildPath "windows_cng.bin"
$sizeInBytes = 1048576  # Exactly 1 MiB (1024 * 1024 bytes)

Write-Host "[*] Windows Random Number Generation (CNG / .NET)" -ForegroundColor Cyan
Write-Host "[*] Target Output File : $outputFile"
Write-Host "[*] Generating $sizeInBytes bytes (1 MiB) of cryptographically secure random data..."

# Allocate 1 MiB byte buffer
$randomBytes = New-Object byte[] $sizeInBytes

# Use Windows Cryptography API via .NET System.Security.Cryptography.RandomNumberGenerator
# Under the hood, this calls BCryptGenRandom (Windows CNG) with BCRYPT_USE_SYSTEM_PREFERRED_RNG
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($randomBytes)

# Write binary data to disk
[System.IO.File]::WriteAllBytes($outputFile, $randomBytes)

# Verify generated file
if (Test-Path -Path $outputFile) {
    $fileInfo = Get-Item -Path $outputFile
    Write-Host "[+] Generation Successful!" -ForegroundColor Green
    Write-Host "[+] File Size: $($fileInfo.Length) bytes ($([math]::Round($fileInfo.Length / 1MB, 2)) MiB)"
} else {
    Write-Error "[-] Failed to generate $outputFile"
}
