# Add Python Scripts to PATH
# This script will add the Python Scripts directory to your PATH variable

$pythonPath = "C:/Users/vland/python-sdk/python3.13.2"
$scriptsPath = "$pythonPath/Scripts"

# Get current user PATH
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

# Check if Scripts path is already in PATH
if ($currentPath -like "*$scriptsPath*") {
    Write-Host "Python Scripts path is already in environment variable" -ForegroundColor Green
} else {
    # Add Scripts path to PATH
    $newPath = $currentPath + ";" + $scriptsPath
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Successfully added Python Scripts path to environment variable" -ForegroundColor Green
    Write-Host "Please close and reopen your terminal for changes to take effect" -ForegroundColor Yellow
}

# Test with full path
Write-Host "`nTesting pip installation:" -ForegroundColor Cyan
& "$scriptsPath/pip.exe" --version

Write-Host "`nSetup completed!" -ForegroundColor Green
