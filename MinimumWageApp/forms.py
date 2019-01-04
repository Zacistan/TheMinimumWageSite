from django import forms

class StateSearch(forms.Form):
    state_name = forms.CharField(label='Name of State', max_length=25)
