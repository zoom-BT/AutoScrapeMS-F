@echo off
REM Lancer Nginx
start "" "C:\nginx\nginx-1.26.2\nginx.exe"

REM Attendre que Nginx démarre (donner un délai de quelques secondes)
timeout /t 10 /nobreak

REM Lancer Waitress en spécifiant le chemin complet
start "" "C:\Users\Administrateur\Documents\ScrapeBot\venv\Scripts\waitress-serve.exe" --host=0.0.0.0 --port=8000 AutoBot.wsgi:application
