# Fix Python Path Priority
# This script will move your Python installation to the front of the PATH variable

$pythonPath = "C:/Users/vland/python-sdk/python3.13.2"

# Get current user PATH
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

# Remove the Python path if it exists (to avoid duplicates)
$cleanedPath = $currentPath -replace [regex]::Escape($pythonPath), ""

# Add Python path to the front
$newPath = $pythonPath + ";" + $cleanedPath.TrimStart(';')

# Set the new PATH
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")

Write-Host "Python path has been moved to the front of PATH variable" -ForegroundColor Green
Write-Host "Please close and reopen your terminal for changes to take effect" -ForegroundColor Yellow

# Test with full path
Write-Host "`nTesting Python installation:" -ForegroundColor Cyan
& "$pythonPath/python.exe" --version
