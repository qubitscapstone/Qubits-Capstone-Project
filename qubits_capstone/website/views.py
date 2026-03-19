from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import website.models
from .forms import PatientForm, VitalsForm

@login_required
def home(request):
    return render(request,"home.html")

## example of creating objects using model is in csv script
## TODO create new_intake view function
def patient_intake(request):
    # if the request a post request (submit button was clicked)
    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        vitals_form = VitalsForm(request.POST)
        if patient_form.is_valid() and vitals_form.is_valid():
           patient = patient_form.save(commit=False)
           patient.save()
           vitals = vitals_form.save(commit=False)
           vitals.save()
           return redirect("intake_success")
    else:
        patient_form = PatientForm()
        vitals_form = VitalsForm()
        all_visits= website.models.Visit.objects.all()
        context = {'all_visits': all_visits, 'patient_form': patient_form, 'vitals_form': vitals_form}
        return render(request,"patient_intake.html", context)