from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    Ajout de champs pour différencier particuliers et professionnels.
    """
    is_individual = models.BooleanField(default=True, verbose_name="Particulier")
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nom de l'entreprise")

    def __str__(self):
        return self.username
