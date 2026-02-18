$WshShell = New-Object -comObject WScript.Shell
$WorkDir = Get-Location
$Target = "dist\Convertly\Convertly.exe"
$Icon = "frontend\assets\logo.ico"
$ShortcutPath = "Convertly.lnk"

# Create Shortcut
$Shortcut = $WshShell.CreateShortcut("$WorkDir\$ShortcutPath")
$Shortcut.TargetPath = "$WorkDir\$Target"
$Shortcut.IconLocation = "$WorkDir\$Icon"
$Shortcut.WorkingDirectory = "$WorkDir\dist\Convertly"
$Shortcut.Save()
Write-Host "Shortcut created: $ShortcutPath"
