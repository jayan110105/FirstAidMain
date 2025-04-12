from django import forms

class QuizScoreForm(forms.Form):
    score = forms.IntegerField(min_value=0)
    module_slug = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        module_slug = kwargs.pop('module_slug', None)
        super().__init__(*args, **kwargs)
        if module_slug:
            self.fields['module_slug'].initial = module_slug