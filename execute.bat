@echo off

:start
cls

python 0_scraper.py%*
timeout /t 3600 /nobreak
tasklist | find /i "python.exe" >NUL && taskkill /f /im "python.exe" || taskkill /f /im "py.exe"

goto start