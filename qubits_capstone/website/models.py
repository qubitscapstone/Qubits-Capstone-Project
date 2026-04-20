from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
#Foriegnkey links two models together 
#meta allows you to configure table level behavior
#str___self determines how it is displayed

#------------------------Shift Information------------------------
class Shift(models.Model):

    shift_id = models.AutoField(primary_key=True)

    shift_name = models.CharField(max_length=6, choices=(('A','a'),('B', 'b'),('C','c')), null=True, blank=True)

    active = models.BooleanField()
    
    def __str__(self):
         return f"{self.shift_name},{self.active}"



#------------------------STAFF Information------------------------

class Staff(models.Model):
    # opted out of years of experience, unnecessary 
    # staff general information 
    staff_id = models.AutoField(primary_key=True)
    
    shift_id = models.ForeignKey(
        'Shift', 
        related_name='shift',
        db_column='shift_id', 
        on_delete=models.PROTECT, 
        default=2
    )

    # (..., null = True, blank = True) allows for those variables to be left null/empty 

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    #title
    specialization = models.CharField(max_length = 50)

    primary_branch = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15)  

    email = models.CharField(max_length= 100, null= True, blank = True)

    # the current csv file only contains Dr.'s, the staff that will use this tool the most will be nurses
    title = models.CharField(max_length=50, null=True , blank= True)

   

    def __str__(self):
         return f"{self.first_name[0]},{self.last_name}, {self.title}"

  


#-----------------------------------Patient Information----------------------------

#Patient Data 
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True) # would we want this to be connected to an MRN?
    
    # Personal Information
    #attributes deleted = contact_number, email, address, insurance_provider, insurance_number

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,  blank=True)
    gender = models.CharField(max_length=6, choices=(('male','Male'),('female', 'Female'),('other','Other')), null=True, blank=True) #our output should say sex, not gender
    
    
     # 1. readable name of the patient
    def get_full_name(self):
        """Returns the patient's full name."""
        return f"{self.first_name} {self.last_name}"


  # Care Team **** ADDED THIS****
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank= True,  
                                limit_choices_to={"title__in": ["Doctor","MD","DO"]},
                                related_name= "doctor_patients")
    nurse = models.ForeignKey(Staff, 
                              on_delete=models.SET_NULL, 
                              limit_choices_to={"title__in": ["Nurse", "RN"]},
                              related_name= "nurse_patients", 
                              #from Bailey: had to add for csv import to work. can delete later
                              null=True,
                              blank=True)
    


  #Should we add final traige score?

    def get_full_name(self):
     return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name()}\n\tAssigned Dr: {self.doctor}\n\tAssigned Nurse: {self.nurse}"   




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

    complaint = models.CharField(blank = True, null = True)
    
    arrival_time = models.DateTimeField(default=timezone.now)
    exiting_time = models.DateTimeField(null=True, blank=True)
        
    # These fields will now be calculated automatically
    queue_count_before_processing = models.IntegerField(default=0, editable=False)
    queue_count_after_processing = models.IntegerField(default=0, editable=False)
    queue_difference = models.IntegerField(null=True, editable=False)

    def save(self, *args, **kwargs):
        # 1. Calculate Queue BEFORE (Patients who arrived but haven't exited yet)
        if not self.visit_id:  # Only calculate on first creation
            self.queue_count_before_processing = Visit.objects.filter(
                arrival_time__lt=self.arrival_time,
                exiting_time__isnull=True
            ).count()

        # 2. Logic when the patient exits
        if self.exiting_time:
            # Calculate Queue AFTER (Others still waiting when this person leaves)
            self.queue_count_after_processing = Visit.objects.filter(
                arrival_time__lt=self.exiting_time,
                exiting_time__isnull=True
            ).exclude(pk=self.visit_id).count()
            
            # Calculate Waiting Time
            if self.arrival_time:
                self.waiting_time = self.exiting_time - self.arrival_time
        
        # 3. Calculate the Difference
        # Logic: If 10 were there before, and 4 are there after, difference is 6
        self.queue_difference = self.queue_count_before_processing - self.queue_count_after_processing
            
        super(Visit, self).save(*args, **kwargs)

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