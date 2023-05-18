from django.db import models
from django.core.validators import MinValueValidator
from django_extensions.db.models import TimeStampedModel


class Orders(TimeStampedModel):
    
    user_id = models.IntegerField()
    
    item_description = models.CharField(max_length=255)
    
    item_quantity = models.PositiveIntegerField()
    
    item_price = models.FloatField(validators=[MinValueValidator(0.0)])
    
    total_value = models.FloatField(validators=[MinValueValidator(0.0)])
