import os
import csv
from .models import StateData

def start_up():
    # Remove all existing data for states
    try:
        StateData.objects.all().delete()

        script_parent_dir = os.path.dirname(__file__)
        state_data_file = os.path.join(script_parent_dir, 'data/StateData.csv')
        with open(state_data_file) as state_data_csv:
            state_data = csv.reader(state_data_csv)
            for counter, row in enumerate(state_data):
                if counter > 0:
                    state_model = StateData()
                    state_model.state_name = row[0]
                    state_model.hourly_min_wage = row[1]
                    state_model.hourly_living_cost = row[2]
                    state_model.save()
    except Exception as e: 
        print(e)
        print("ERROR: Unable to populate data in database.")