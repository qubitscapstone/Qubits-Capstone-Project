print("Starting ESI triage script")
import os
import psycopg


# DATABASE_URL comes from Neon Console . 'postgresql://neondb_owner:npg_JaIUMi7c1KWw@ep-square-cell-ajy3vwcs.c-3.us-east-2.aws.neon.tech/neondb?sslmode=require'
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to get ESI Level for a given Vitals_id
def get_esi_for_vital_id(Vitals_id):
    """
    Given Vitals_id, read vitals from Neon and return ESI level as a string:
        "Level 1", "Level 2", ..., "Level 5"
    """
    # 1) Connect to Neon and get vitals for this Vitals_id
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT "Heart_rate", "Systolic_blood_pressure", "Oxygen_saturation",
                       "Body_temperature", "Pain_level", "Chronic_disease_count"
                FROM "website_vitals"
                WHERE "Vitals_id" = %s
            """, (Vitals_id,))
            row = cur.fetchone()

    if row is None:
        raise ValueError(f"Vitals_id {Vitals_id} not found")

    # 2) Unpack the vitals
    hr, sys_bp, pulse_ox, body_temp, pain_level, chronic_disease = row

    # 3) Arrays to collect concerns per level (Level 1–5)
    lvl_1 = []
    lvl_2 = []
    lvl_3 = []
    lvl_4 = []
    lvl_5 = []

    # 4) Ask user if patient is stable
    print("Is the patient stable?")
    user_input = input("Enter y/n/o: ").strip().lower()

    if user_input == 'n':
        # Unstable → immediate concern
        lvl_1.append("Patient requires immediate medical attention")

    elif user_input == 'y':
        # Stable → check vitals

        if hr < 60 or hr > 160:
            lvl_2.append("Heart Rate")
        if sys_bp > 150 or sys_bp < 100:
            lvl_2.append("Blood Pressure")
        if pulse_ox < 90:
            lvl_2.append("Pulse Oximetry < 90")
        elif pulse_ox < 95 and pulse_ox >= 92:
            lvl_3.append("Pulse Oximetry 92–94")
        if body_temp > 100 or body_temp < 95:
            lvl_2.append("Body Temperature")
        if pain_level >= 7:
            lvl_2.append("Pain Level >= 7")
        elif pain_level >= 4:
            lvl_3.append("Pain Level 4–6")
        elif pain_level >= 0:
            lvl_4.append("Pain Level 0–3")
        if chronic_disease > 2:
            lvl_2.append("Chronic Disease > 2")
        elif chronic_disease > 0:
            lvl_3.append("Chronic Disease 1–2")

    elif user_input == 'o':
        # Manual override: user types the level
        esi_input = input("Enter 1/2/3/4/5: ").strip()
        return f"Level {esi_input}"

    # 5) Decide final ESI level from the lists
    if len(lvl_1) > 0:
        esi_level = "Level 1"
    elif len(lvl_2) > 0:
        esi_level = "Level 2"
    elif len(lvl_3) > 0:
        esi_level = "Level 3"
    elif len(lvl_4) > 0:
        esi_level = "Level 4"
    else:
        esi_level = "Level 5"

    # 6) Print what triggered each level
    print("Level 1:", ", ".join(lvl_1) if lvl_1 else "empty")
    print("Level 2:", ", ".join(lvl_2) if lvl_2 else "empty")
    print("Level 3:", ", ".join(lvl_3) if lvl_3 else "empty")
    print("Level 4:", ", ".join(lvl_4) if lvl_4 else "empty")
    print("Level 5:", ", ".join(lvl_5) if lvl_5 else "empty")

    # 7) RETURN the ESI level (for the view.py)
    return esi_level


# --- CONSOLE ENTRY POINT (fixed indentation and position) ---
if __name__ == "__main__":
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set.")
        print("Run:")
        print("  export DATABASE_URL='your_neon_url'")
        exit(1)

    try:
        Vitals_id = int(input("Enter Vitals_id: "))
        level = get_esi_for_vital_id(Vitals_id)
        print(f"\nESI level for Vitals_id {Vitals_id}: {level}")
    except ValueError as e:
        print(e)
