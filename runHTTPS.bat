cd \D "%~dp0"

python frontend\skeleton-bot\configs.py true
cd frontend\skeleton-bot
start cmd /k ng serve --host 0.0.0.0 --port 12547 --disable-host-check --ssl true
cd ../../backend
venv\Scripts\python.exe main.py https
pause