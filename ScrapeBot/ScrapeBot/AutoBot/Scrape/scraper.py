from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import errors
import logging

# Assurez-vous d'importer vos fonctions de notification si elles sont dans un autre fichier
# from .notifier import get_recipient_emails, send_email

logger = logging.getLogger(__name__)

async def scrape_data(url, collection):
    logger.info(f"Début du scraping pour l'URL : {url}")
    async with async_playwright() as p:
        # headless=True est recommandé pour l'automatisation, False pour le débogage
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, timeout=300000)
        except Exception as e:
            logger.error(f"[Main URL Error] Impossible de charger {url} — {e}")
            await browser.close()
            return

        await page.wait_for_load_state('load')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Votre logique pour trouver les liens sur la page principale
        divs = [
            soup.find_all('a', class_="vacanciesTableLink vacanciesTable__row"),
            soup.find_all('div', class_="td-block-row"),
            soup.find_all('tr', class_="ng-star-inserted"),
            soup.find_all('tr', class_='even') + soup.find_all('tr', class_='odd')
        ]
        
        count_updated = 0

        for div_group in divs:
            for x in div_group:
                lien = x.find('a') if x.find('a') else x
                link_url = lien.get('href') if lien and lien.has_attr('href') else None
                
                if not link_url:
                    continue

                offer_url = urljoin(url, link_url)
                
                try:
                    logger.debug(f"Visite de la sous-page : {offer_url}")
                    await page.goto(offer_url, timeout=300000)
                    content1 = await page.content()
                    soup1 = BeautifulSoup(content1, 'html.parser')

                    title = soup1.find('h1') or soup1.find('h2')
                    title1 = title.get_text(strip=True) if title else 'Titre non trouvé'

                    paragraphs = soup1.find_all('p') or soup1.find_all('td')
                    description = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)

                    entry = {
                        "link": offer_url,
                        "titre": title1,
                        "description": description,
                        "timestamp": datetime.now()
                    }

                    # --- LOGIQUE DE MISE À JOUR (UPSERT) ---
                    # Met à jour le document s'il existe, ou le crée s'il n'existe pas.
                    collection.update_one(
                        {"link": offer_url},  # Le critère pour trouver le document
                        {"$set": entry},      # Les données à mettre à jour ou à insérer
                        upsert=True           # L'option qui crée le document si non trouvé
                    )
                    
                    logger.info(f"SUCCÈS : Donnée sauvegardée/mise à jour -> Titre : {entry['titre']}")
                    count_updated += 1

                except Exception as e:
                    logger.error(f"[ERROR] Impossible d'accéder ou de traiter {offer_url}: {e}")

        await browser.close()
        logger.info(f"Scraping terminé pour {url}. {count_updated} éléments ont été ajoutés ou mis à jour.")

        # if count_updated > 0:
        #     send_alert_email(count_updated)

# def send_alert_email(count):
#     recipients = get_recipient_emails()
#     if recipients:
#         subject = f"{count} nouvelles entrées ajoutées"
#         body = f"Appel d'offre trouvées ! {count} nouvelles opportunités d'appel d'offres ajoutées."
#         send_email(recipients, subject, body)