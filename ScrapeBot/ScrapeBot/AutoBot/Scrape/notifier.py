import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
import time
from datetime import datetime

# Configurer MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["DBscrapeBot"]
collection = db["scrape"]

# Adresse e-mail de l'expéditeur
sender_email = "emmanuelranava.megasoft@gmail.com"
sender_password = "ekyereuucrzfssty"

# Fonction pour envoyer un email
def send_email(recipients, subject, body):
    for recipient in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connexion au serveur SMTP de Gmail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient, text)
            server.quit()
            print(f"Notification envoyée à {recipient}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email à {recipient}: {e}")

# Fonction pour vérifier les nouvelles entrées
 #Fonction pour vérifier les nouvelles données et envoyer une notification
def check_new_entries():
    latest_check = datetime.now()
    while True:
        new_entries = collection.find({"timestamp": {"$gt": latest_check}})
        count = new_entries.count()

        if count > 0:
            latest_check = datetime.now()
            recipients = get_recipient_emails()
            if recipients:
                subject = f"{count} nouvelles opportunités"
                body = f"{count} nouvelles opportunités d'appel d'offres trouvées et ajoutées."
                send_email(recipients, subject, body)
        else:
            # Notification si aucune nouvelle donnée n'est trouvée
            recipients = get_recipient_emails()
            if recipients:
                subject = "Aucune nouvelle donnée ajoutée"
                body = "Le scraping est terminé ! Aucune nouvelle opportunités d'appel d'offres n'a été trouvées et ajoutées."
                send_email(recipients, subject, body)

        time.sleep(60)

def get_recipient_emails():
    email_collection = db["emails"]
    emails = email_collection.find()
    return [email["email"] for email in emails]

if __name__ == "__main__":
    check_new_entries()