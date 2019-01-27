from django.db import models

# Create your models here.
class StateData(models.Model):
    state_name = models.CharField(max_length=25)
    hourly_min_wage = models.DecimalField(max_digits=20,decimal_places=2)
    hourly_living_cost = models.DecimalField(max_digits=20,decimal_places=2)

    def check_if_state_is_valid(state_name):
        if not StateData.objects.filter(state_name=state_name.upper()):
            raise Exception('State not found in database.')