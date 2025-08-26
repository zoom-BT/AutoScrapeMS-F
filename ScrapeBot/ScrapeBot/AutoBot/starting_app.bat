@echo on

REM Start Nginx
start "" "C:\nginx\nginx-1.26.2\nginx.exe" -p "C:\nginx\nginx-1.26.2"

timeout /t 10 /nobreak

REM Set working directory to the project root
cd /d "C:\Users\Administrateur\Documents\ScrapeBot"

REM Ensure Python can find project modules
set PYTHONPATH=C:\Users\Administrateur\Documents\ScrapeBot

REM Launch Waitress with the full WSGI path
"C:\Users\Administrateur\Documents\ScrapeBot\venv\Scripts\waitress-serve.exe" --host=0.0.0.0 --port=8000 AutoBot.wsgi:application

pause
