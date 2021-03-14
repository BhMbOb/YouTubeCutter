cd /D "%~dp0"
call venv\scripts\activate
python -m main.py
call venv\scripts\deactivate
pause