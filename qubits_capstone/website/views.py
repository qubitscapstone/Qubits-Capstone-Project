from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models

@login_required
def home(request):
    return render(request,"home.html")

def in_building(request):
    all_visits= website.models.Visit.objects.all()
    context = {'all_visits': all_visits}
    return render(request,"in_building.html", context)

## example of creating objects using model is in csv script
## TODO create new_intake view function
    # if the request a post request (submit button was clicked)
        # create new patient object
        # create new vitals object
    # else (request is a get request)
        # return page render 