import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

companies = pd.read_csv(os.path.join(DATA_DIR, "companies.csv"))

roles = [
    "Software Engineer",
    "SDE",
    "Data Analyst",
    "Data Scientist",
    "AI Engineer",
    "ML Engineer",
    "Business Analyst",
    "Consultant",
    "Cyber Security Analyst",
    "Cloud Engineer",
    "DevOps Engineer",
    "Product Engineer",
    "Embedded Engineer",
    "VLSI Engineer"
]

locations = [
    "Bangalore",
    "Hyderabad",
    "Gurgaon",
    "Noida",
    "Pune",
    "Chennai",
    "Mumbai"
]

drives = []

drive_id = 101

for _ in range(250):

    company = companies.sample(1).iloc[0]

    ctc = round(random.uniform(8, 50), 2)

    if ctc >= 35:
        min_cgpa = round(random.uniform(8.2, 9.0), 2)
    elif ctc >= 20:
        min_cgpa = round(random.uniform(7.5, 8.3), 2)
    else:
        min_cgpa = round(random.uniform(6.5, 7.5), 2)

    hiring_type = random.choices(
        ["Full-Time", "Internship", "PPO"],
        weights=[60, 25, 15]
    )[0]

    drives.append({

        "drive_id": drive_id,

        "company_id": company["company_id"],

        "role": random.choice(roles),

        "hiring_type": hiring_type,

        "ctc": ctc,

        "minimum_cgpa": round(min_cgpa,2),

        "location": random.choice(locations),

        "drive_date":
        f"2026-{random.randint(8,10):02d}-{random.randint(1,28):02d}"

    })

    drive_id += 1

df = pd.DataFrame(drives)

df.to_csv(os.path.join(DATA_DIR, "placement_drives.csv"), index=False)

print(df.head())

print("Placement Drives Generated:", len(df))