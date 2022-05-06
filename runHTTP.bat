cd \D "%~dp0"

python frontend\skeleton-bot\configs.py false
cd frontend\skeleton-bot
start cmd /k runhttp.bat
title "bot [http]"
cd ../../backend
venv\Scripts\python.exe main.py
pause