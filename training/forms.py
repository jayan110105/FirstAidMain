# Add this to your forms.py file
from django import forms

class QuizScoreForm(forms.Form):
    score = forms.IntegerField(widget=forms.HiddenInput())
    time_spent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    module_slug = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, module_slug=None, **kwargs):
        super().__init__(*args, **kwargs)
        if module_slug:
            self.fields['module_slug'].initial = module_slug

class ScenarioScoreForm(forms.Form):
    score = forms.IntegerField(widget=forms.HiddenInput())
    time_spent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    scenario_slug = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, scenario_slug=None, **kwargs):
        super().__init__(*args, **kwargs)
        if scenario_slug:
            self.fields['scenario_slug'].initial = scenario_slug
