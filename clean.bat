@ECHO off
echo Cleaning...
del /S /Q *.pyc

set /P c=Remove .CSV file? [y/n]
if /I "%c%" EQU "y" goto :rmcsv
goto :next

:rmcsv
echo Removing .csv ...
del /S /Q *.csv

:next
set /P c=Remove database file? [y/n]
if /I "%c%" EQU "y" goto :rmdb
goto :end

:rmdb
echo Removing db ...
del /S /Q *.db

:end 
echo Done!
pause