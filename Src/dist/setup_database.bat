@echo off
set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 8.0\bin"
set ENV_FILE=.env
for /f "tokens=1,2 delims==" %%a in (%ENV_FILE%) do (
    if "%%a"=="DB_NAME" set DB_NAME=%%b
    if "%%a"=="DB_USER" set DB_USER=%%b
    if "%%a"=="DB_PASSWORD" set DB_PASSWORD=%%b
)
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u %DB_USER% -p%DB_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u %DB_USER% -p%DB_PASSWORD% %DB_NAME% < schema.sql
echo Database setup complete!
pause