import asyncio
from .scraper import scrape_data
from apscheduler.schedulers.background import BlockingScheduler

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['DBscrapeBot']
collection = db['scrape']


def scrape(urls):
    """Fonction de scraping à exécuter par le planificateur."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for url in urls:
        loop.run_until_complete(scrape_data(url, collection))
    loop.close()

def schedule_scraping(urls, time_str):
    """Planifier le scraping à l'heure spécifiée."""
    scheduler = BlockingScheduler()
    scheduler.add_job(scrape, 'cron', hour=time_str.hour, minute=time_str.minute, args=[urls])
    scheduler.start()