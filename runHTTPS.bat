cd \D "%~dp0"

python frontend\skeleton-bot\configs.py true
cd frontend\skeleton-bot
start cmd /k run.bat
title "bot [https]"
cd ../../backend
venv\Scripts\python.exe main.py https
pause