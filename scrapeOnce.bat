@echo off
python 0_scraper.py%*
tasklist | find /i "python.exe" >NUL && taskkill /f /im "python.exe" || taskkill /f /im "py.exe"
