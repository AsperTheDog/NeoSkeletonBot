cd \D "%~dp0"

python configs/setup.py
pause
cd backend
pip install virtualenv
virtualenv venv
venv\Scripts\pip3.exe install -r requirements.txt
venv\Scripts\python.exe ..\configs\certsGenerator.py
cd ../frontend/skeleton-bot
call npm install -g @angular/cli
call npm install
pause