from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
#Foriegnkey links two models together 
#meta allows you to configure table level behavior
#str___self determines how it is displayed

#------------------------STAFF Information______________________________

class Staff(models.Model):
    # opted out of years of experience, unnecessary 
    # staff general information 
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    #title
    speacialization = models.CharField(max_length = 50)
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
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20) #our output should say sex, not gender
    
    
    # Administrative Data
    registration_date = models.DateTimeField(auto_now_add=True)
   

     # 1. readable name of the patient
    def get_full_name(self):
        """Returns the patient's full name."""
        return f"{self.first_name} {self.last_name}"


  # Care Team **** ADDED THIS****
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank= True,  
                                limit_choices_to={"title__in": ["Doctor","MD","DO"]},
                                related_name= "doctor_patients")
    nurse = models.ForeignKey(Staff, on_delete=models.SET_NULL, 
                                limit_choices_to={"title__in": ["Nurse", "RN"]},
                                                  related_name= "nurse_patients")
    


  #Should we add final traige score?

    def get_full_name(self):
     return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name()}\n\tAssigned Dr: {self.doctor}\n\tAssigned Nurse: {self.nurse}"   

#-----------------------------------Vitals---------------------------------------


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
    
    waiting_time = models.DurationField(null=True, blank=True, editable=False)
    
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
 
    #--------------------------------------Triage-------------------------------------

class TriageAssessment(models.Model):
    triage_id = models.AutoField(primary_key=True)
    
    visit_id = models.ForeignKey(
        'Visit', 
        on_delete=models.CASCADE, 
        related_name='triage_assessments',
        db_column='visit_id'
    )
    
    # Updated to point to the Staff model
    staff_id = models.ForeignKey( #is this for who is completing the assessemnt?
        'Staff', 
        on_delete=models.PROTECT, # Prevents deleting staff if they have linked records
        db_column='staff_id'
    )
    
    triage_time = models.DateTimeField(default=timezone.now)
    complaint = models.TextField()
    
    pain_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"Triage {self.triage_id} by {self.staff_id}"

class Triage_scores(models.Model):
    # Primary Key - Auto-incrementing
    score_id = models.AutoField(primary_key=True)
    
    # Link to Triage Assessment
    triage_id = models.ForeignKey(
        'TriageAssessment', 
        on_delete=models.CASCADE, 
        related_name='scores',
        db_column='triage_id'
    )
    
    # ESI Level (1 to 5)
    esi_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Description of resources
    resources_needed = models.TextField()
    
    # Link to Staff (assigned_by)
    assigned_by = models.ForeignKey(
        'Staff', 
        on_delete=models.PROTECT,
        db_column='assigned_by' # Sets the database column name exactly
    )

    def __str__(self):
        return f"ESI Level {self.esi_level} assigned by {self.assigned_by}



#-----------------------------Vitals----------------------------------------

class Vitals(models.Model):
    heart_rate = models.IntegerField()
    systolic_blood_pressure = models.IntegerField()
    oxygen_saturation= models.IntegerField()
    body_temperature= models.DecimalField(max_digits=4, decimal_places=1)
    pain_level=models.IntegerField()
    chronic_disease_count = models.IntegerField()

    time_of_vitals = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f" Vitals were recorded at {self.time_of_vitals} \n\t HR: {self.heart_rate} \n\t Systolic BP: {self.systolic_blood_pressure} \n\t Pulse Ox:{self.oxygen_saturation} \n\t Body Temp:{self.body_temperature} \n\t Reported Painlevel:{self.pain_level}"

    class Meta:
        ordering = ['time_of_vitals']
        verbose_name_plural = "Vitals"





    





    