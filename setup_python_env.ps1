# Python Environment Setup Script
$pythonPath = "C:/Users/vland/python-sdk/python3.13.2"

# Check if Python path exists
if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Python path does not exist: $pythonPath" -ForegroundColor Red
    exit 1
}

# Get current system environment variable
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

# Check if Python path is already in environment variable
if ($currentPath -like "*$pythonPath*") {
    Write-Host "Python path is already in environment variable" -ForegroundColor Green
} else {
    # Add Python path to environment variable
    $newPath = $currentPath + ";" + $pythonPath
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Successfully added Python path to environment variable" -ForegroundColor Green
    Write-Host "Please close and reopen terminal for changes to take effect" -ForegroundColor Yellow
}

# Display current Python version
Write-Host "`nTesting Python installation:" -ForegroundColor Cyan
& "$pythonPath/python.exe" --version

Write-Host "`nEnvironment variable setup completed!" -ForegroundColor Green
