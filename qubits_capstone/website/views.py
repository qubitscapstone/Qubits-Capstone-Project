from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models
from .forms import PatientForm, VitalsForm, HighRiskForm, PatientLeftForm, SwitchShiftForm, AddStaffToShiftForm, AssignNursetoPatient
from django.contrib import messages
from .webapp_scripts.esi_logic import get_esi_for_vital_id


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def patient_intake(request):
    
    # gather data needed for all requests 
    all_assessments = website.models.TriageAssessment.objects.order_by('-triage_id')

    patient_form = PatientForm()
    high_risk_form = HighRiskForm()
    vitals_form = VitalsForm()
    patient_left_form = PatientLeftForm()

    context = {
        "all_assessments": all_assessments,
        "patient_form": patient_form,
        "high_risk_form": high_risk_form,
        "vitals_form": vitals_form,
        "patient_left_form" : patient_left_form, 
        "ESI_score" : None,
        "open_high_risk" : False,
        "open_vitals" : False,
        "open_ESI_output" : False
    }   

    if request.method == "POST":

        if "patient_submit" in request.POST:
            patient_form = PatientForm(request.POST)
            if patient_form.is_valid():
                patient = patient_form.save()

                # create a visit for the patient immediately. (updates the table)
                visit = website.models.Visit.objects.create(patient_id = patient)

                # save the visit id created to use in vitals creation
                request.session['current_visit_id'] = visit.visit_id

                # open the high risk modal
                context["open_high_risk"] = True

            else:
                print(patient_form.errors)

        elif "high_risk_submit" in request.POST:
            high_risk_form = HighRiskForm(request.POST)
            if high_risk_form.is_valid():

                # get visit and save the complaint to it
                # visit_primary_key = request.session.get("current_visit_id")
                # visit = website.models.Visit.objects.get(visit_id=visit_primary_key)
                # visit.complaint = high_risk_form.cleaned_data["complaint"]
                # visit.save()

                # save in session to be used when vital is created
                request.session['life_saving_intervention'] = high_risk_form.cleaned_data["life_saving_intervention"]
                request.session['high_risk'] = high_risk_form.cleaned_data["high_risk"]
                request.session['disoriented'] = high_risk_form.cleaned_data["disoriented"]
                request.session['severe_pain'] = high_risk_form.cleaned_data["severe_pain"]
                request.session['diff_resources'] = high_risk_form.cleaned_data["diff_resources"]

                # open vitals modal
                context["open_vitals"] = True

            else:
                print(high_risk_form.errors)
        
        elif "vitals_submit" in request.POST:
            vitals_form = VitalsForm(request.POST)
            if vitals_form.is_valid():
                # save data from form
                curr_vitals = vitals_form.save(commit=False)

                # get visit object
                visit_primary_key = request.session.get("current_visit_id")
                current_visit = website.models.Visit.objects.get(visit_id=visit_primary_key)
                curr_vitals.visit_id = current_visit

                # save data from session data from previous modals
                curr_vitals.life_saving_intervention = request.session.get("life_saving_intervention")
                curr_vitals.high_risk = request.session.get("high_risk")
                curr_vitals.disoriented = request.session.get("disoriented")
                curr_vitals.severe_pain = request.session.get("severe_pain")
                curr_vitals.diff_resources = request.session.get("diff_resources")

                # commit vitals to db
                curr_vitals.save()

                # get the score if they manually entered it
                context["ESI_score"] = vitals_form.cleaned_data.get("esi_override")

                #TO DO: Get ESI script data to the database and front end
                # # if no override, calculate using script
                if not context["ESI_score"]:
                    context["ESI_score"] = get_esi_for_vital_id(curr_vitals.Vitals_id)

                # save ESI score in DB
                website.models.TriageAssessment.objects.create(vitals_id=curr_vitals, esi_level = context["ESI_score"])

                # after everything has saved, remove saved session values to avoid errors in later entries
                request.session.pop('current_visit_id', None)    
                request.session.pop('life_saving_intervention', None) 
                request.session.pop('high_risk', None) 
                request.session.pop('disoriented', None) 
                request.session.pop('severe_pain', None) 
                request.session.pop('diff_resources', None) 

                # open the ESI output modal
                context["open_ESI_output"] = True

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

    return render(request, "patient_intake.html", context)


@login_required
def shift(request):
    # Load all staff members (for shift dropdowns)
    all_staff = website.models.Staff.objects.all()
    active_shift = website.models.Shift.objects.get(active=True)
    
    # Initialize empty forms (will be populated on POST or used in template)
    switch_shift_form = SwitchShiftForm()
    add_staff_form = AddStaffToShiftForm()
    
    # Base context with data for template rendering
    context = {          # List of nurses for display/dropdowns
        "all_staff": all_staff,             # All staff for shift management
        "active_shift": active_shift,
        "switch_shift_form": switch_shift_form,  # Form for changing shifts
        "add_staff_form": add_staff_form,   # Form for adding staff to shifts
        "message": None                     # Success/error messages
    }
    
    # Handle form submissions (exact same pattern as patient_intake)
    if request.method == "POST":
        
        # CASE 1: User clicked save in "Add staff to shift"
        if "add_staff_submit" in request.POST:
            # Re-create form with POST data for validation
            add_staff_form = AddStaffToShiftForm(request.POST)
            
            # Validate form data (handles field validation, required fields)
            if add_staff_form.is_valid():
                # Extract cleaned data (safe, validated values)
                staff = add_staff_form.cleaned_data['staff_to_add']
                
                # Safely get staff record by ID (like patient_left_form)
                try: 
                    staff.shift_id = active_shift
                    staff.save()
                    
                    # Success message (shows in template)
                    context["message"] = "Staff added to shift!"
                    
                    # Reset form for next use
                    add_staff_form = SwitchShiftForm()
                    
                except website.models.Staff.DoesNotExist:
                    # Handle case where staff ID doesn't exist
                    context["message"] = "Staff not found."
            else:
                # Form errors (invalid shift choice, missing staff_id, etc.)
                print(add_staff_form.errors)  
                
        # CASE 2: User clicked "switch shift" button  
        elif "switch_shift_submit" in request.POST:
            # Re-create form with POST data
            switch_shift_form = SwitchShiftForm(request.POST)
            
            if switch_shift_form.is_valid():
                new_active_id = switch_shift_form.cleaned_data['new_shift']
                
                # set old shift to not active anymore
                active_shift.active = False;
                active_shift.save()

                # set new active shift
                new_active = website.models.Shift.objects.get(shift_id=new_active_id)
                new_active.active = True
                new_active.save()
                context["active_shift"] = new_active

                # Success feedback
                context["message"] = "Shift updated successfully!"
                
                # Reset form
                add_staff_form = SwitchShiftForm()
            else:
                print(add_staff_form.errors) 
                
    # render shift.html with updated context
    return render(request, "shift.html", context)

@login_required
def nurse_workload(request):
    all_assessments = website.models.TriageAssessment.objects.order_by('-triage_id')
    all_staff = website.models.Staff.objects.all()
    assign_patient = AssignNursetoPatient()
    context = {
        "all_assessments": all_assessments,
        "all_staff": all_staff, 
        "assign_patient": assign_patient
    } 
    return render(request, "nurse_workload.html", context)