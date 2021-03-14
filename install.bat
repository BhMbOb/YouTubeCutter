cd /D "%~dp0"
pip install virtualenvwrapper
python -m venv venv
call venv\scripts\activate
pip3 install -U -r requirements.txt
call venv\scripts\deactivate