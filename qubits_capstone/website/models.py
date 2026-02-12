from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    
    # Contact Details
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    
    # Administrative Data
    registration_date = models.DateTimeField(auto_now_add=True)
    insurance_provider = models.CharField(max_length=150)
    insurance_number = models.CharField(max_length=50)

     # 1. readable name of the patient
    def get_full_name(self):
        """Returns the patient's full name."""
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
