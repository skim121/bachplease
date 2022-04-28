from django import forms 
from .models import *
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit, Layout, Row, Column 

class DayEventForm(forms.ModelForm): 
    class Meta: 
        model = DayEvent 
        fields = ['schedule', 'event', 'day']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))
            
            # self.fields['event'].queryset = Event.objects.filter(city=schedule.city)
            # self.fields['schedule'].queryset = Schedule.objects.all()
            # self.fields['event'].queryset= Event.objects.none()
            # if 'schedule' in self.data: 
            #     try: 
            #         schedulecity = self.data.get(schedule.city)
            #         self.fields['event'].queryset = Event.objects.filter(city=schedulecity).values_list('name', flat=True).order_by('name')
            #     except (ValueError, TypeError): 
            #         pass
            

            # customq= Event.objects.filter(city = schedule.city)
            # self.fields['events'].queryset=customq
            # self.helper = FormHelper()
            # 
        