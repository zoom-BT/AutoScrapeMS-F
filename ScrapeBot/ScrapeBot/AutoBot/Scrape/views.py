from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import EmailForm, CustomUserCreationForm, CustomAuthenticationForm
from .scraper import scrape_data
from .scheduler import schedule_scraping  # Assurez-vous d'importer votre fonction de planification
from pymongo import MongoClient
import asyncio
from datetime import datetime
from .notifier import send_email 
import csv
import pandas as pd
from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json
from django.core.paginator import Paginator


# Initialisation du scheduler pour la planification
scheduler = BackgroundScheduler()
scheduler.start()

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBscrapeBot']
collection = db['scrape']
email_collection = db["emails"]



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # Correction ici
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Nom d’utilisateur ou mot de passe incorrect.')  # Message d'erreur
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
        # Nombre d'utilisateurs inscrits
    user_count = User.objects.count()

    # Nombre de données dans la collection MongoDB
    data_count = collection.count_documents({})

    # Nombre d'emails enregistrés pour recevoir des alertes
    email_count = email_collection.count_documents({})

    # Passer les données au template
    return render(request, 'home.html', {
        'user_count': user_count,
        'data_count': data_count,
        'email_count': email_count
    })


# Vue pour enregistrer les e-mails
@login_required
def register_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Enregistrer l'email dans MongoDB
            email_collection.insert_one({"email": email})
            return render(request, 'email_success.html', {'email': email})
    else:
        form = EmailForm()

    return render(request, 'register_email.html', {'form': form})

@login_required
def dashboard_view(request):
    # Nombre d'utilisateurs inscrits
    user_count = User.objects.count()

    # Nombre de données dans la collection MongoDB
    data_count = collection.count_documents({})

    # Nombre d'emails enregistrés pour recevoir des alertes
    email_count = email_collection.count_documents({})

    # Passer les données au template
    return render(request, 'dashboard.html', {
        'user_count': user_count,
        'data_count': data_count,
        'email_count': email_count
    })

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
                subject = f"{count} nouvelles entrées ajoutées"
                body = f"{count} nouvelles opportunités d'appel d'offres trouvées et ajoutées."
                send_email(recipients, subject, body)
        else:
            # Notification si aucune nouvelle donnée n'est trouvée
            recipients = get_recipient_emails()
            if recipients:
                subject = "Aucune nouvelle donnée ajoutée"
                body = "Appel d'offre trouvées ! nouvelles opportunités d'appel d'offres n'a été trouvées et ajoutées."
                send_email(recipients, subject, body)

        time.sleep(60)

def get_recipient_emails():
    email_collection = db["emails"]
    emails = email_collection.find()
    return [email["email"] for email in emails]


@login_required
def scrape_view(request):
    if request.method == 'POST':
        url_input = request.POST.get('url_input', '')
        
        if not url_input:
            return render(request, 'scrape.html', {'warning': "⚠️ Veuillez entrer au moins une URL."})
        
        urls = [url.strip() for url in url_input.split(',')]
        
        async def run_scraping():
            for url in urls:
                # Appel à scrape_data avec l'URL et la collection
                await scrape_data(url, collection)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_scraping())
        
        return render(request, 'scrape.html', {'success': "✅ Scraping terminé pour toutes les URL !"})

    return render(request, 'scrape.html')  # Affiche le formulaire si la méthode n'est pas POST

@login_required
def scrape_affiche(request):
    # Charger les données une seule fois
    scraped_data = list(collection.find())

    if not scraped_data:
        return render(request, 'affiche.html', {'info': "ℹ️ Pas de données disponibles."})

    # Convertir les données en DataFrame
    df = pd.DataFrame(scraped_data)

    # Assurez-vous que la colonne 'link' est présente et formatée
    if 'link' in df.columns:
        df['link'] = df['link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # Trier par date si la colonne 'timestamp' existe
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Conversion en datetime
        df = df.sort_values(by='timestamp', ascending=False)  # Tri décroissant

    # Suppression des tooltips pour la cellule de description
    for col in df.columns:
        df[col] = df[col].apply(lambda x: f'<span>{x}</span>')  # Affichage simple sans tooltip

    # Pagination
    paginator = Paginator(df.values, 20)  # 20 lignes par page
    page_number = request.GET.get('page', 1)  # Obtenir le numéro de page depuis l'URL, par défaut 1
    page_obj = paginator.get_page(page_number)

    # Conversion des données paginées en HTML pour affichage
    data_html = pd.DataFrame(page_obj.object_list, columns=df.columns).to_html(classes='table table-striped', index=False, escape=False)

    return render(request, 'affiche.html', {'data_html': data_html, 'page_obj': page_obj})


@login_required
def scrape_export(request):
    # Exporter les données scrapées
    if request.method == 'POST' and 'export_data' in request.POST:
        scraped_data = list(collection.find())
        
        if not scraped_data:
            return render(request, 'export.html', {'info': "ℹ️ Pas de données disponibles pour l'exportation."})
        
        file_format = request.POST.get('file_format', 'CSV')
        
        if file_format == "CSV":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="data.csv"'
            pd.DataFrame(scraped_data).to_csv(path_or_buf=response, index=False)
            return response
        
        elif file_format == "JSON":
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="data.json"'
            json_data = json.dumps(scraped_data, default=str)  # Utiliser default=str pour gérer les objets BSON
            response.write(json_data)
            return response
        
        elif file_format == "Excel":
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            pd.DataFrame(scraped_data).to_excel(excel_writer=response, index=False)
            return response
    
    # Si la méthode n'est pas POST, retourner une page par défaut ou un message
    return render(request, 'export.html')
@login_required
def scrape_planifie(request):
    # Planification du scraping
    if request.method == 'POST' and 'schedule_scraping' in request.POST:
        url_input = request.POST.get('url_input', '')
        time_input = request.POST.get('time_input', '')

        if not url_input:
            return render(request, 'planifie.html', {'warning': "⚠️ Veuillez entrer au moins une URL."})

        urls = [url.strip() for url in url_input.split(',')]

        try:
            # Convertir l'heure en un objet datetime.time
            time_obj = datetime.strptime(time_input, '%H:%M').time()

            # Appeler la fonction de planification ici avec l'heure convertie
            asyncio.run(schedule_scraping(urls, time_obj))
            
            return render(request, 'planifie.html', {'success': f"✅ Scraping planifié pour {time_obj} pour les URL : {', '.join(urls)}."})
        except ValueError:
            return render(request, 'planifie.html', {'warning': "⚠️ Format de l'heure invalide. Utilisez HH:MM."})

    return render(request, 'planifie.html')

# Dans views.py
def stop_scheduler():
    # Code pour arrêter le scheduler
    pass


