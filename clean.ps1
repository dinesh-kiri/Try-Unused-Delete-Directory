# clean.ps1
Write-Host "🚀 Auto Cleaner Started..."

$scriptUrl = "https://github.com/dinesh-kiri/Try-Unused-Delete-Directory/blob/main/cleaner.py"
$localFile = "$env:TEMP\cleaner.py"

Invoke-WebRequest -Uri $scriptUrl -OutFile $localFile

# Run Python Script
python $localFile --delete
