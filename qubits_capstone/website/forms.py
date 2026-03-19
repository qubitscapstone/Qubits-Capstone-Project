from django import forms
from .models import Patient, Vitals

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['patient_id', 'doctor', 'nurse']

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        exclude = ['Vitals_id', 'Triage_id', 'Time_of_vitals']