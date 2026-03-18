from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models
## import the two forms form forms.py

@login_required
def home(request):
    return render(request,"home.html")

## example of creating objects using model is in csv script
## TODO create new_intake view function
def patient_intake(request):
    # if the request a post request (submit button was clicked)
    # create new patient object
    # create new vitals object
    # else (request is a get request)
        # return page render (include the lines below this)
    all_visits= website.models.Visit.objects.all()
    context = {'all_visits': all_visits}    
    # be sure to add the form into this below
    return render(request,"patient_intake.html", context)