from website.models import Vitals 

def calculate_esi():
    score = 0

    #passing imported values from CSV to algorithm 
    heart_rate = Vitals.heart_rate
    systolic_blood_pressure = Vitals.systolic_blood_pressure
    oxygen_saturation= Vitals.oxygen_saturation
    body_temperature= Vitals.body_temperature
    pain_level= Vitals.pain_level
    chronic_disease_count = Vitals.chronic_disease_count


    print("Is the patient stable?\n")

    user_input = input("Enter y/n")[0]

    if user_input[0] == 'n' | 'N':
        score = 10
    while user_input[0] == 'y' | 'Y':
        if heart_rate < 60 | heart_rate >160:
            score+=3
        elif heart_rate >60 | heart_rate < 160:
            score =+1
        if systolic
        


        

