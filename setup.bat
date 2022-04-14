pip install pyOpenSSL
python certsGenerator.py
cd backend
pip install virtualenv
virtualenv venv
venv\Scripts\pip3.exe install -r ..\backend\requirements.txt
cd ../frontend/skeleton-bot
call npm install -g @angular/cli
call npm install
python configs/setup.py
pause