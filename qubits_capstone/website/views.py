from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models
from .forms import PatientForm, VitalsForm, HighRiskForm, PatientLeftForm
from django.contrib import messages
# from .webapp_scripts.esi_logic import get_esi_for_vital_id


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def patient_intake(request):
    all_visits = website.models.Visit.objects.all()

    if request.method == "POST":
        if "patient_submit" in request.POST:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                patient = patient_form.save()

                # create a visit for the patient immediately. (updates the table)
                visit = website.models.Visit.objects.create(patient_id = patient)

                # save the visit id created to use in vitals creation
                request.session['current_visit_id'] = visit.visit_id

            else:
                print(patient_form.errors)

        elif "high_risk_submit" in request.POST:
            high_risk_form = HighRiskForm(request.POST)
            if high_risk_form.is_valid():

                # get visit and save the complaint to it
                visit_primary_key = request.session.get("current_visit_id")
                visit = website.models.Visit.objects.get(visit_id=visit_primary_key)
                visit.complaint = high_risk_form.cleaned_data["complaint"]
                visit.save()

                # save in session to be used when vital is created
                request.session['life_saving_intervention'] = high_risk_form.cleaned_data["life_saving_intervention"]
                request.session['high_risk'] = high_risk_form.cleaned_data["high_risk"]
                request.session['disoriented'] = high_risk_form.cleaned_data["disoriented"]
                request.session['severe_pain'] = high_risk_form.cleaned_data["severe_pain"]
                request.session['diff_resources'] = high_risk_form.cleaned_data["diff_resources"]

            else:
                print(high_risk_form.errors)
        
        elif "vitals_submit" in request.POST:
            vitals_form = VitalsForm(request.POST)
            if vitals_form.is_valid():
                # save data from form
                curr_vitals = vitals_form.save(commit=False)

                # get visit object
                visit_primary_key = request.session.get("current_visit_id")
                curr_vitals.visit_id = website.models.Visit.objects.get(visit_id=visit_primary_key)

                # save data from session data from previous modals
                curr_vitals.life_saving_intervention = request.session.get("life_saving_intervention")
                curr_vitals.high_risk = request.session.get("high_risk")
                curr_vitals.disoriented = request.session.get("disoriented")
                curr_vitals.severe_pain = request.session.get("severe_pain")
                curr_vitals.diff_resources = request.session.get("diff_resources")

                # commit vitals to db
                curr_vitals.save()

                # get the score if they manually entered it
                esi_score = vitals_form.cleaned_data.get("esi_override")

                # # if no override, calculate using script
                # if not esi_score:
                #     esi_score = get_esi_for_vital_id(curr_vitals.Vitals_id)

                # # after obtaining level, save assessment and score
                # curr_assessment = website.models.TriageAssessment.objects.create(vitals_id = curr_vitals, visit_id = curr_visit)
                # website.models.Triage_scores.objects.create(triage_id=curr_assessment, esi_level = esi_score)

                # after everything has saved, remove saved session values to avoid errors in later entries
                request.session.pop('current_visit_id', None)    
                request.session.pop('life_saving_intervention', None) 
                request.session.pop('high_risk', None) 
                request.session.pop('disoriented', None) 
                request.session.pop('severe_pain', None) 
                request.session.pop('diff_resources', None) 

            else:
                print(vitals_form.errors)

        elif "patient_left_submit" in request.POST:
            patient_left_form = PatientLeftForm(request.POST)
            if patient_left_form.is_valid():
                patient_that_left_id = patient_left_form.cleaned_data['patient_id']
                # try to make sure patient exists
                try:
                    patient_that_left = website.models.Patient.objects.get(patient_id=patient_that_left_id)
                    
                    # delete patient
                    patient_that_left.delete()
                    messages.success(request, "Patient has been deleted.")

                except website.models.Patient.DoesNotExist:
                    messages.error(request, "Patient does not exist.")

            else:
                print(patient_left_form.errors)

    patient_form = PatientForm()
    high_risk_form = HighRiskForm()
    vitals_form = VitalsForm()
    patient_left_form = PatientLeftForm()

    context = {
        "all_visits": all_visits,
        "patient_form": patient_form,
        "high_risk_form": high_risk_form,
        "vitals_form": vitals_form,
        "patient_left_form" : patient_left_form
    }
    return render(request, "patient_intake.html", context)