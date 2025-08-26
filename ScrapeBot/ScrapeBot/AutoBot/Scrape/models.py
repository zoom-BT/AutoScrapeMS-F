from django.db import models

class Site(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    last_scraped = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class EmailRecipient(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
class DataModel(models.Model):
    # Définir les champs du modèle
    title = models.CharField(max_length=200)  # Un champ de texte pour le titre
    description = models.TextField()           # Un champ de texte pour la description
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)      # Date de mise à jour
    is_active = models.BooleanField(default=True)          # Champ pour l'état actif/inactif

    class Meta:
        verbose_name = "Your Data"
        verbose_name_plural = "Your Data List"
        ordering = ['-created_at']  # Triez par date de création décroissante

    def __str__(self):
        return self.title  # Retourne le titre lors de l'affichage de l'objet
