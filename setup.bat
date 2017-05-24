@ECHO off

:choice
set /P c=Are you sure you want to setup the database (THIS WILL ERASE THE ORIGINAL DB)[y/n]?
if /I "%c%" EQU "y" goto :ifyes
if /I "%c%" EQU "n" goto :otherwise
goto :choice

:ifyes
echo Setting up database, config
python create_db.py
echo DONE
goto :end

:otherwise
echo Abort

:end
pause 
exit

