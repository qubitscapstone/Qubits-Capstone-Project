website.models import Vitals
 
def run():
    score = 0
 
    #passing imported values from CSV to algorithm
    #heart_rate = Vitals.heart_rate
    # systolic_blood_pressure = Vitals.systolic_blood_pressure
    # oxygen_saturation= Vitals.oxygen_saturation
    # body_temperature= Vitals.body_temperature
    # pain_level= Vitals.pain_level
    # chronic_disease_count = Vitals.chronic_disease_count
    # we should include pulse rate,
 
    #will not need these lines after UI is implemented
    print("Is the patient stable?\n")
 
    user_input = input("Enter y/n")[0] #console input
# Basic Vital Score Calculations
    if user_input[0] == 'n' or 'N':
        score = 10
    elif user_input[0] == 'y' or 'Y': # need to learn how to connect this to Popup window
        if Vitals.heart_rate < 60 or Vitals.heart_rate >160:
            score+=1
        if Vitals.Systolic_blood_pressure > 150 or Vitals.Systolic_blood_pressure < 100:
            score += 1
        if Vitals.Oxygen_saturation < 90:
            score += 1
        elif Vitals.Oxygen_saturation < 94 or Vitals.Oxygen_saturation >=91:
            score += .5
        if Vitals.Body_temperature > 100 or Vitals.Body_temperature < 95:
            score += 1
        if Vitals.Pain_level >= 8 : # what about neurological concerns when you do not feel anything
            score += 1
        if Vitals.Chronic_disease_count >= 1:
            score += .5 # should we have this reiterate for each disease? Ask Joey
        #if Vitals.Respiration_Rate > 20 or  Vitald.Respriation_Rate < 12:
            #score +=1
    else:
        user_input = input # what would the input of this be, since it would be coming form the front end
        # maybe a recursive loop
 
# these create a base score 5.5
#special cases
if Vitals.heart_rate < 60 and Vitals.Systolic_blood_pressure < 100:
    score +=2
if Vitals.Body_temperature > 100 and Vitals.Heart_rate > 120:
    score += 2
if Vitals.Oxygen_saturation < 90 and Vitals.Heart_rate < 50:
    score += 1
if Vitals.Oxygen_saturation < 90 and Vitals.Heart_rate < 50 and Vitals.Systolic_blood_pressure < 100:
    score += 2
 
# do we want to create a trend algorithm? Ask Group on Tuesday
#print("The Patient's final score is:\t", score,"/10")