import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_esi_for_vital_id(Vitals_id):
    """
    Given Vitals_id, read vitals from Neon and return ESI level as integer:
        1, 2, 3, 4, or 5
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    "Heart_rate",
                    "Systolic_blood_pressure",
                    "Oxygen_saturation",
                    "Body_temperature",
                    "Pain_level",
                    "Chronic_disease_count",
                    "disoriented",
                    "high_risk",
                    "life_saving_intervention",
                    "severe_pain",
                    "Respiratory_rate"
                FROM "website_vitals"
                WHERE "Vitals_id" = %s
            """, (Vitals_id,))
            row = cur.fetchone()

    if row is None:
        raise ValueError(f"Vitals_id {Vitals_id} not found")

    (
        hr,
        sys_bp,
        pulse_ox,
        body_temp,
        pain_level,
        chronic_disease,
        disoriented,
        high_risk,
        life_saving_intervention,
        severe_pain,
        respiratory_rate,
    ) = row

    lvl_1 = []
    lvl_2 = []
    lvl_3 = []
    lvl_4 = []
    lvl_5 = []

    # Check Level 1: Life saving intervention
    if life_saving_intervention == 1:
        lvl_1.append("Requires immediate lifesaving intervention")

    # Check Level 2: High risk, disoriented, severe pain
    if high_risk == 1:
        lvl_2.append("High-risk situation")
    if disoriented == 1:
        lvl_2.append("Confused/lethargic/disoriented")
    if severe_pain == 1:
        lvl_2.append("Severe pain/distress")

    # Vital signs checks
    if hr is not None and (hr < 60 or hr > 160):
        lvl_2.append("Heart Rate")
    if sys_bp is not None and (sys_bp > 150 or sys_bp < 100):
        lvl_2.append("Blood Pressure")
    if pulse_ox is not None:
        if pulse_ox < 90:
            lvl_2.append("Pulse Oximetry < 90")
        elif 92 <= pulse_ox < 95:
            lvl_3.append("Pulse Oximetry 92–94")
    if body_temp is not None and (body_temp > 100 or body_temp < 95):
        lvl_2.append("Body Temperature")
    if respiratory_rate is not None and (respiratory_rate < 10 or respiratory_rate > 24):
        lvl_2.append("Respiratory Rate")
    if pain_level is not None:
        if pain_level >= 7:
            lvl_2.append("Pain Level >= 7")
        elif pain_level >= 4:
            lvl_3.append("Pain Level 4–6")
        elif pain_level >= 0:
            lvl_4.append("Pain Level 0–3")
    if chronic_disease is not None:
        if chronic_disease > 2:
            lvl_2.append("Chronic Disease > 2")
        elif chronic_disease > 0:
            lvl_3.append("Chronic Disease 1–2")

    # Determine final level as numeric
    if len(lvl_1) > 0:
        esi_level = 1
    elif len(lvl_2) > 0:
        esi_level = 2
    elif len(lvl_3) > 0:
        esi_level = 3
    elif len(lvl_4) > 0:
        esi_level = 4
    else:
        esi_level = 5

    return esi_level

if __name__ == "__main__":
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set.")
        print("Run:")
        print("  export DATABASE_URL='your_neon_url'")
        exit(1)

    try:
        Vitals_id = int(input("Enter Vitals_id: "))
        level = get_esi_for_vital_id(Vitals_id)
        # Returns numeric: 1, 2, 3, 4, or 5
    except ValueError as e:
        print(e)