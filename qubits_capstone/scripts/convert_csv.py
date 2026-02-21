import pandas as pd
from website.models import Patient, Visit, Vitals, Staff

def run():
    df = pd.read_csv('qubits_capstone/data/patients.csv')

    for i, row in df.iterrows():
        Patient.objects.create(
            first_name = row["First_name"],
            last_name = row["Last_name"],
            date_of_birth = pd.to_datetime(row["Date_of_birth"]).date(),
            gender = row["Gender"],
        )
    print("Patients imported successfully.")

    df = pd.read_csv('qubits_capstone/data/Staff.csv')

    for i, row in df.iterrows():
        Staff.objects.create(
            first_name = row["First_name"],
            last_name = row["Last_name"],
            specialization = row["Specialization"],
            phone_number = row["Phone_number"],
            primary_branch=row["Hospital_branch"],
            email = row["Email"],
            title="Doctor"
        )
    print("Staff imported successfully.")

    df = pd.read_csv('qubits_capstone/data/Triage_Vitals.csv')

    # for i, row in df.iterrows():
    #     Vitals.objects.create(
    #         Triage_id_id = row["Triage_id"],
    #         Age = row["Age"],
    #         Heart_rate = row["Heart_rate"], 
    #         Systolic_blood_pressure = row["Systolic_blood_pressure"],
    #         Oxygen_saturation = row["Oxygen_saturation"],
    #         Body_temperature = row["Body_temperature"],
    #         Pain_level = row["Pain_level"],
    #         Chronic_disease_count = row["Chronic_disease_count"],
    #     )
    # print("Vitals imported successfully.")

    df = pd.read_csv('qubits_capstone/data/Visit.csv')

    for i, row in df.iterrows():
        Visit.objects.create(
           patient_id_id = row["Patient_ID"],
           arrival_time = pd.to_datetime(row["Arrival_Time"]),
           exiting_time = pd.to_datetime(row["Exiting_Time"]),
        )
    print("Visits imported successfully.")