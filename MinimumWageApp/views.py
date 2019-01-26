from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape

from .forms import StateSearch
from .models import StateData
from .modules.convertStateCode import convert_two_letter_state_code

# Landing page
def index(request):
    state_search_form = StateSearch()
    return render(request, 'MinimumWageApp/index.html', {'state_search_form': state_search_form})

# Redirects user to page for their state based on the form. 
def redirect_to_state(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StateSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            state = str(escape(form.cleaned_data['state_name']))
            try:
                # Exception is thrown if no state is found for two letter code.
                if len(state) == 2:
                    state = convert_two_letter_state_code(two_letter_code=state.upper())
                # Exception is thrown if state is not found in database.
                if not StateData.objects.filter(state_name=state.upper()):
                    raise Exception('State not found in database.')
            except Exception as e:
                print('An exception was thrown: {0}'.format(e))
                form.add_error(field='state_name', error="State name is invalid.")
                return render(request, 'MinimumWageApp/index.html', {'state_search_form': form})
                
            return HttpResponseRedirect('/state/{0}'.format(state))
        else:
            print('Form is invalid.\n Form error:{0}'.format(form.errors.as_text))

    return HttpResponseRedirect('/')

def render_state_data(request, state_name):
    # Exception is thrown if state is not found in database.
    state_data = (StateData.objects.filter(state_name=state_name.upper()))[0]
    # Hourly wage * 40 hours a week * 52 weeks in a year * 2 people
    annual_min_wage_for_two = state_data.hourly_min_wage * 40 * 52 * 2
    minwage_livingcost_difference = state_data.yearly_living_cost - annual_min_wage_for_two
    template_variables = {
        'state_name': state_data.state_name.capitalize(),
        'annual_min_wage_for_two': '${:,.2f}'.format(annual_min_wage_for_two),
        'minwage_livingcost_difference': '${:,.2f}'.format(minwage_livingcost_difference),
        'hourly_min_wage': '${:,.2f}'.format(state_data.hourly_min_wage),
        'annual_family_living_wage': '${:,.2f}'.format(state_data.yearly_living_cost),
    }
    state_search_form = StateSearch()
    return render(request, 'MinimumWageApp/state_data.html', {'state_data': template_variables, 'state_search_form': state_search_form})