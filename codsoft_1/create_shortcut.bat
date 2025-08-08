@echo off
echo Creating desktop shortcut for TaskMaster Pro...

:: Get the current directory
set "CURRENT_DIR=%~dp0"

:: Create a shortcut on the desktop
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\TaskMaster Pro.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%run.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.IconLocation = '%CURRENT_DIR%app_icon.svg,0'; $Shortcut.Save()"

echo Shortcut created successfully!
echo You can now launch TaskMaster Pro from your desktop.

pause