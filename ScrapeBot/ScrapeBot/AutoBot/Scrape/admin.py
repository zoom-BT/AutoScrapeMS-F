from django.contrib import admin
from .models import Site, User, EmailRecipient

# Configuration de l'affichage du modèle Site
class SiteAdmin(admin.ModelAdmin):
    # Affichage de ces colonnes dans la liste des objets
    list_display = ('title', 'url', 'last_scraped')
    # Champs pour lesquels activer la recherche dans l'admin
    search_fields = ('title', 'url')
    # Champs pour filtrer les objets dans l'interface d'administration
    list_filter = ('last_scraped',)
    # Champs en lecture seule (non modifiables via l'interface)
    readonly_fields = ('last_scraped',)

# Configuration de l'affichage du modèle User
class UserAdmin(admin.ModelAdmin):
    # Afficher les colonnes dans la liste des utilisateurs
    list_display = ('username', 'first_name', 'last_name', 'email')
    # Recherche possible sur ces champs
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Configuration de l'affichage du modèle EmailRecipient
class EmailRecipientAdmin(admin.ModelAdmin):
    # Afficher l'email dans la liste des objets
    list_display = ('email',)
    # Recherche par email
    search_fields = ('email',)

# Enregistrement des modèles avec leur configuration personnalisée
admin.site.register(Site, SiteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(EmailRecipient, EmailRecipientAdmin)
