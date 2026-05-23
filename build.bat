@echo off
REM Build single-file exe with PyInstaller
REM Run from project root: build.bat

pip install pyinstaller -q
pyinstaller --noconfirm --onefile --windowed ^
    --name "UpdateTools" ^
    --icon "NONE" ^
    --add-data "app;app" ^
    main.py

echo.
echo Done! Output: dist\UpdateTools.exe
pause
