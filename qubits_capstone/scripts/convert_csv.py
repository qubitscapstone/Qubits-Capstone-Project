import pandas as pd
from website.models import Patient, Visit, Triage_Vitals, Triage_Scores, Staff

def run():
    # TODO : update var names & test (probably clean data as well)
    # created before models and final CSVs

    df = pd.read_csv('data/patient.csv')

    for i, row in df.iterrows():
        Patient.objects.create(
            # add row.get(col_name) for non-required 
            Patient_id = row["Patient_id"],
            First_name = row["First_name"],
            Last_name = row["Last_name"],
            Date_Of_Birth = row["Date_of_birth"],
            Gender = row["Gender"],
            Contact_number = row["Contact_number"],
            Address = row["Address"],
            Registration_date = row["Registration_date"],
            Insurance_provide = row["Insurance_provider"],
            Insurance_number = row["Insurance_number"],
            Email = row["Email"]
        )

    df = pd.read_csv('data/Staff.csv')

    for i, row in df.iterrows():
        Staff.objects.create(
            Staff_id = row["Staff_id"],
            First_name = row["First_name"],
            Last_name = row["Last_name"],
            Specialization = row["Specialization"],
            Phone_number = row["Phone_number"],
            Years_experience = row["Years_experience"],
            Hospital_branch = row["Hospital_branch"],
            Email = row["Email"]
        )

    df = pd.read_csv('data/Triage_Vitals.csv')

    for i, row in df.iterrows():
        Triage_Vitals.objects.create(
            Vitals_id = row["Vitals_id"],
            Triage_id = row["Triage_id"],
            Age = row["Age"],
            Heart_rate = row["Heart_rate"], 
            Systolic_blood_pressure = row["Systolic_blood_pressure"],
            Oxygen_saturation = row["Oxygen_saturation"],
            Body_temperature = row["Body_temperature"],
            Pain_level = row["Pain_level"],
            Chronic_disease_count = row["Chronic_disease_count"],
            Previous_er_visits = row["Previous_er_visits"],
            Arrival_mode = row["Arrival_mode"],
            Triage_level = row["Triage_level"]
        )
    df = pd.read_csv('data/Visit.csv')

    for i, row in df.iterrows():
        Visit.objects.create(
           Visit_id = row["Visit_id"],
           Patient_id = row["Patient_id"],
           Arrival_time = row["Arrival_time"],
           Exiting_Time = row["Exiting_Time"],
           Waitng_Time = row["Waitng_Time"],
           Queue_Count_Before_Processing = row["Queue_Count_Before_Processing"],
           Queue_Count_After_Processing = row["Queue_Count_After_Processing"],
           Queue_Difference = row["Queue_Difference"]
        )

    df =pd.read_csv('data.Triage_Scores.csv')

    for i, row in df.iterrows():
        Triage_Scores.objects.create(
            Score_id = row["Score_id"],
            Triage_id = row["Triage_id"],
            Esi_level = row["Esi_level"],
            Resources_needed = row["Resources_needed"],
            Assigned_by = row["Assigned_by"]
        )