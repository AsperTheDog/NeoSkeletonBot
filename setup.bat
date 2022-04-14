cd \D "%~dp0"

pip install openssl
python certsGenerator.py
cd backend
pip install virtualenv
virtualenv venv
venv\Scripts\pip3.exe install -r ..\backend\requirements.txt
cd ../frontend/skeleton-bot
npm install
pause