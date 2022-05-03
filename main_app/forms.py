from django import forms 
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *

class DateInput(forms.DateInput):
    input_type = 'date'

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule 
        fields = ['name', 'date_in', 'date_out', 'numdays', 'city']
        widgets = {
            'date_in': DateInput(),
            'date_out': DateInput(),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

class ScheduleUpdateForm(forms.ModelForm):
    class Meta:
        model = Schedule 
        fields = ['name', 'date_in', 'date_out', 'numdays']
        widgets = {
            'date_in': DateInput(),
            'date_out': DateInput(),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))

class DayEventForm(forms.ModelForm): 

    class Meta: 
        model = DayEvent 
        fields = ['schedule', 'event', 'day']
        
        # widgets = {'schedule': widgets.Select(attrs={'disabled':'disabled'})}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # if self.fields['days'] >= self.fields['schedule'].numdays:
            #     raise forms.ValidationError("Type the correct day")

            self.filters['schedule'].field.widget.attrs.update({'class': 'form-select'})
            self.filters['event'].field.widget.attrs.update({'class': 'form-select'})
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))