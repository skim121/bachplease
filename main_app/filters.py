import django_filters
from django import forms 
from django.contrib.auth.models import User 
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *


class EventFilter(django_filters.FilterSet): 
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(), empty_label=None)
    tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta: 
        model = Event
        fields = ['city', 'tag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('type')
            )
        )
        # self.fields['city'].empty_label = None


class CityFilter(django_filters.FilterSet): 
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(), empty_label=None)
    budget = django_filters.MultipleChoiceFilter(choices=(
            ('Free', 'Free'),
            ('$', '$'),
            ('$$', '$$'),
            ('$$$', '$$$'),
            ('$$$$','$$$$'),
            ), required=False)
    tag = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)

    class Meta: 
        model = Event
        fields = ['city', 'budget', 'tag']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'search-form'
        self.helper.form_class = 'search-filter-form mb-4'
        self.helper.form_method='GET'
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Fieldset(
                'legend',
                'city',
                'budget',
                'tag'
            ),
            # InlineCheckboxes('tag', css_class = 'tag-checkboxes')
        )

   
    