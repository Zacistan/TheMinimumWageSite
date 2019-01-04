from django.db import models

# Create your models here.
class StateData(models.Model):
    state_name = models.CharField(max_length=25)
    hourly_min_wage = models.DecimalField(max_digits=20,decimal_places=2)
    yearly_living_cost = models.DecimalField(max_digits=20,decimal_places=2)