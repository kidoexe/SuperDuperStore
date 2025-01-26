from django.db.models import TextChoices
class Currency(TextChoices):
    Gel = "gel", "₾"
    USD = 'usd', "$"
    EURO = 'euri', "€"