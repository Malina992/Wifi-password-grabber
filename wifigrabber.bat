@echo off
setlocal enabledelayedexpansion

set "baseName=wynik"
set "extension=.txt"
set "output=%baseName%%extension%"


if exist "%output%" (
    set "counter=1"
    :checkNext

    set /a "formatted=1000+counter"
    set "suffix=!formatted:~-3!"
    set "output=%baseName%!suffix!%extension%"
    
    if exist "!output!" (
        set /a "counter+=1"
        goto :checkNext
    )
)

echo Saving to file: %output%
echo --- Wyniki netsh --- > "%output%"

for /f "tokens=2 delims=:" %%A in ('netsh wlan show profiles ^| findstr /C:"All User Profile"') do (
    
    
    set "profileName=%%A"
   
    set "profileName=!profileName:~1!"

    echo Przetwarzanie: !profileName!
    
    echo. >> "%output%"
    echo ===== Profil: !profileName! ===== >> "%output%"
    

    netsh wlan show profile name="!profileName!" key=clear >> "%output%"
)

echo.
echo Passwords saved in: %output%
