from django import forms
from .models import Patient, Vitals

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'gender': 'Sex',
        }

        widgets = {
            'first_name' : forms.TextInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),

            'last_name' : forms.TextInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),

            'date_of_birth' : forms.DateInput( 
                attrs={ 
                    'class': 'form-control', 
                    'type': 'date',
                    'required': True, } ),

            'gender': forms.Select( 
                attrs={ 
                    'class': 'form-select', 
                    'required': True, } )
        }

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields=['Age', 'Heart_rate', 'Systolic_blood_pressure', 'Oxygen_saturation', 'Body_temperature', 'Pain_level', 'Chronic_disease_count']
        labels={
            'Age' : 'Age', 
            'Heart_rate' : 'Heart rate', 
            'Systolic_blood_pressure' : 'Systolic blood pressure', 
            'Oxygen_saturation' : 'Oxygen saturation', 
            'Body_temperature' : 'Body temperature', 
            'Pain_level' : 'Pain level', 
            'Chronic_disease_count':'Chronic disease count'
        }
        widgets={
            'Age' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),

            'Heart_rate' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),

            'Systolic_blood_pressure' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),

            'Oxygen_saturation': forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),
            'Body_temperature' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),
            'Pain_level' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } ),
            'Chronic_disease_count' : forms.NumberInput( 
                attrs={ 
                    'class': 'form-control', 
                    'required': True, } )
        }