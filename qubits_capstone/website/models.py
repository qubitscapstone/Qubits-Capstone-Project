from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

#------------------------Shift Information------------------------
class Shift(models.Model):

    shift_id = models.AutoField(primary_key=True)

    shift_name = models.CharField(max_length=6, choices=(('A','a'),('B', 'b'),('C','c')), null=True, blank=True)

    active = models.BooleanField()
    
    def __str__(self):
         return f"{self.shift_name},{self.active}"



#------------------------STAFF Information------------------------

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    
    shift_id = models.ForeignKey(
        'Shift', 
        related_name='shift',
        db_column='shift_id', 
        on_delete=models.PROTECT, 
        default=1
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15)  

    email = models.CharField(max_length= 100, null= True, blank = True)
   
    def __str__(self):
         return f"{self.first_name} {self.last_name}"

#-----------------------------------Patient Information----------------------------

#Patient Data 
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True) # would we want this to be connected to an MRN?

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,  blank=True)
    gender = models.CharField(max_length=6, choices=(('male','Male'),('female', 'Female'),('other','Other')), null=True, blank=True) #our output should say sex, not gender
    
    def get_full_name(self):
        """Returns the patient's full name."""
        return f"{self.first_name} {self.last_name}"

    nurse = models.ForeignKey(Staff, 
                              on_delete=models.SET_NULL, 
                              related_name= "nurse_patients", 
                              null=True,
                              blank=True)
    def __str__(self):
        return f"{self.get_full_name()}\n\tAssigned Nurse: {self.nurse}"   

#------------------------------------Visit Model-----------------------------
class Visit(models.Model):
    # Primary Key - Auto-incrementing
    visit_id = models.AutoField(primary_key=True) #Django creates its own IDs
    
    # Patient link
    patient_id = models.ForeignKey(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='visits',
        db_column='patient_id'
    )
    
    arrival_time = models.DateTimeField(default=timezone.now)
    exiting_time = models.DateTimeField(null=True, blank=True)
            

    def __str__(self):
        return f"Visit {self.visit_id} (Queue Before: {self.queue_count_before_processing})"
    
#-----------------------------Vitals----------------------------------------

class Vitals(models.Model):
    Vitals_id = models.AutoField(primary_key=True)

    visit_id = models.ForeignKey(
        'Visit', 
        on_delete=models.CASCADE, 
        related_name='vitals',
        db_column='visit_id'
    )

    Age = models.IntegerField(blank = True, null=True)
    Heart_rate = models.IntegerField(blank = True,  null=True)
    Systolic_blood_pressure = models.IntegerField(blank = True, null=True)
    Oxygen_saturation= models.IntegerField(blank = True, null=True)
    Body_temperature= models.DecimalField(max_digits=4, decimal_places=1, blank = True, null=True)
    Pain_level=models.IntegerField(blank = True, null=True)
    Chronic_disease_count = models.IntegerField(blank = True, null=True)
    Respiratory_rate = models.IntegerField(blank = True, null=True)
    life_saving_intervention = models.IntegerField(null=True)
    high_risk = models.IntegerField(null=True)
    disoriented = models.IntegerField(null=True)
    severe_pain = models.IntegerField(null=True)
    diff_resources = models.IntegerField(null=True)

    Time_of_vitals = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f" Vitals were recorded at {self.time_of_vitals} \n\t HR: {self.heart_rate} \n\t Systolic BP: {self.systolic_blood_pressure} \n\t Pulse Ox:{self.oxygen_saturation} \n\t Body Temp:{self.body_temperature} \n\t Reported Painlevel:{self.pain_level}"

    class Meta:
        ordering = ['Time_of_vitals']
        verbose_name_plural = "Vitals"
 
    #--------------------------------------Triage-------------------------------------

class TriageAssessment(models.Model):
    triage_id = models.AutoField(primary_key=True)
    
    vitals_id = models.ForeignKey(
        'Vitals', 
        on_delete=models.CASCADE, 
        related_name='triage_assessments',
        db_column='vitals_id'
    )
    
    triage_time = models.DateTimeField(default=timezone.now)
     
    # ESI Level (1 to 5)
    esi_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null = True
    )

    def __str__(self):
        return f"ESI Level {self.esi_level}."