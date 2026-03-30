from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models
from .forms import PatientForm, VitalsForm


@login_required
def home(request):
    return render(request, "home.html")


def patient_intake(request):
    all_visits = website.models.Visit.objects.all()

    if request.method == "POST":
        if "patient_submit" in request.POST:
            patient_form = PatientForm(request.POST)
            vitals_form = VitalsForm()
            if patient_form.is_valid():
                patient_form.save()
            else:
                print(patient_form.errors)

        elif "vitals_submit" in request.POST:
            patient_form = PatientForm()
            vitals_form = VitalsForm(request.POST)
            if vitals_form.is_valid():
                vitals_form.save()
            else:
                print(vitals_form.errors)
        else:
            patient_form = PatientForm()
            vitals_form = VitalsForm()
    else:
        patient_form = PatientForm()
        vitals_form = VitalsForm()

    context = {
        "all_visits": all_visits,
        "patient_form": patient_form,
        "vitals_form": vitals_form,
    }
    return render(request, "patient_intake.html", context)