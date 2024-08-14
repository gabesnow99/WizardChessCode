@echo off
:: Create VBScript file
set "vbsFile=%temp%\run_python_silently.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%vbsFile%"
echo WshShell.Run "cmd /c ""python GUI.py""", 0, False >> "%vbsFile%"
echo Set WshShell = Nothing >> "%vbsFile%"

:: Execute the VBScript file
cscript //nologo "%vbsFile%"

:: Clean up the VBScript file
del "%vbsFile%"

:: Exit the batch file
exit
