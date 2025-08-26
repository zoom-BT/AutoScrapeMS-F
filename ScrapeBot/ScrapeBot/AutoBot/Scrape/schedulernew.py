import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore  # Pour stocker les jobs en DB (optionnel)
from pymongo import MongoClient
from .scraper import scrape_data

# Configuration MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBscrapeBot']
collection = db['scrape']

# URLs à scraper (à personnaliser)
URLS_TO_SCRAPE = [
    "https://example.com/page1",
    "https://example.com/page2",
]

def scrape():
    """Fonction wrapper pour exécuter le scraping en asynchrone."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for url in URLS_TO_SCRAPE:
        loop.run_until_complete(scrape_data(url, collection))
    loop.close()

def schedule_scraping():
    """Démarre le scheduler pour exécuter le scraping chaque jour à 14h30."""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")  # Optionnel : stockage en base Django
    
    # Planifie l'exécution quotidienne à x heure
    scheduler.add_job(
        run_scraping,
        'cron',
        hour=14,
        minute=30,
        id="daily_scraping_job"
    )
    
    scheduler.start()

# Appeler schedule_scraping() au démarrage de l'application Django (voir ci-dessous)