from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import website.models

@login_required
def home(request):
    return render(request,"home.html")

def broken_table(request):
    all_visits= website.models.Visit.objects.all()
    visits= {'all_visits': all_visits}
    return render(request,"broken_table.html", visits)