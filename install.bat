@ECHO off
REM This is the batch file to install necessary files on the target machine

pip install -r requirements.txt

echo.
echo.
echo.

call setup.bat
