from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import errors
from .notifier import get_recipient_emails, send_email





async def scrape_data(url, collection):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_load_state('load')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')


        # Vérification de la catégorie
        category_div = soup.find('div', class_='postMetadata_category')
        if category_div:
            category_text = category_div.get_text(strip=True)
            if "ITB-Appel d'offres" not in category_text:
                print("Cette page n'est pas de catégorie ITB-Appel d'offres.")
                await browser.close()
                return  # Sortie de la fonction si la catégorie ne correspond pas

        divs = [
            soup.find_all('a', class_="vacanciesTableLink vacanciesTable__row"),
            soup.find_all('div', class_="td-block-row"),
            soup.find_all('tr', class_="ng-star-inserted"),
            soup.find_all('tr', class_='even') + soup.find_all('tr', class_='odd')
        ]
        count_new_entries = 0  # Compteur pour les nouvelles entrées

        for index, div_group in enumerate(divs):
            for x in div_group:
                lien = x.find('a') if x.find('a') else x
                link_url = lien['href'] if lien else None
                if link_url:
                    offer_url = urljoin(url, link_url)

                    if collection.find_one({"link": offer_url}):
                        continue

                    try:
                        await page.goto(offer_url, wait_until="networkidle", timeout=100000)
                        await page.wait_for_load_state('load')
                        content1 = await page.content()
                        soup1 = BeautifulSoup(content1, 'html.parser')

                        title = soup1.find('h1') or soup1.find('h2')
                        title1 = title.get_text(strip=True) if title else 'No title'

                        paragraphs = soup1.find_all('p') or soup1.find_all('td')
                        description = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)

                        entry = {
                            "link": offer_url,
                            "titre": title1,
                            "description": description,
                            "timestamp": datetime.now()  
                        }

                        try:
                            collection.insert_one(entry)
                            count_new_entries += 1  # Incrémenter le compteur
                        except errors.DuplicateKeyError:
                            print(f"Document avec l'URL {offer_url} existe déjà, insertion ignorée.")

                    except Exception as e:
                        print(f"Erreur lors de l'accès à {offer_url}: {e}")

        await browser.close()

        # Envoyer l'alerte après le scraping
        if count_new_entries > 0:
            send_alert_email(count_new_entries)


def send_alert_email(count):
    recipients = get_recipient_emails()  # Récupérer les adresses e-mail
    if recipients:
        subject = f"{count} nouvelles entrées ajoutées"
        body = f"appel d'offre trouvées! {count} nouvelles opportunités d'appel d'offres trouvées et ajoutées."
        send_email(recipients, subject, body)
