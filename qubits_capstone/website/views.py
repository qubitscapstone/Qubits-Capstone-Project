from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import website.models
from .forms import PatientForm, VitalsForm

@login_required
def home(request):
    return render(request,"home.html")

def patient_intake(request):
    if request.method == "POST":
        #which submit button was clicked?
        if 'patient_submit' in request.POST:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                patient = patient_form.save(commit=False)
                patient.save()
        elif 'vitals_submit' in request.POST:
            vitals_form = VitalsForm(request.POST)
            if vitals_form.is_valid():
                vitals = vitals_form.save(commit=False)
                vitals.save()
        # return redirect("intake_success")         ----- we do not have this page yet
        #just refreshes the page for now until we get sucess messages
        return render(request,"patient_intake.html", context)
    else:
        patient_form = PatientForm()
        vitals_form = VitalsForm()
        all_visits= website.models.Visit.objects.all()
        context = {'all_visits': all_visits, 'patient_form': patient_form, 'vitals_form': vitals_form}
        return render(request,"patient_intake.html", context)