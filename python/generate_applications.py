import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

students = pd.read_csv(os.path.join(DATA_DIR, "students.csv"))
drives = pd.read_csv(os.path.join(DATA_DIR, "placement_drives.csv"))

applications = []
application_id = 1

for _, student in students.iterrows():

    if student["placement_status"] != "Eligible":
        continue

    possible_drives = drives[
        drives["minimum_cgpa"] <= student["cgpa"]
    ]

    if len(possible_drives) == 0:
        continue

    num_applications = random.randint(
        min(5, len(possible_drives)),
        min(12, len(possible_drives))
    )

    selected = possible_drives.sample(num_applications)

    for _, drive in selected.iterrows():

        resume_score = (
            0.45 * student["resume_score"] +
            0.35 * student["coding_score"] +
            0.20 * (student["cgpa"] * 10)
        )

        if resume_score >= 82:

            oa = int(
                max(
                    0,
                    min(
                        100,
                        student["coding_score"] + random.randint(-10, 10)
                    )
                )
            )

            if oa >= 70:

                interview = (
                    student["communication_score"]
                    + random.randint(-10, 10)
                )

                if interview >= 70:
                    status = random.choices(
                        ["Offered", "Accepted"],
                        weights=[20, 80]
                    )[0]
                else:
                    status = "Rejected"

            else:
                status = "Rejected"

        else:
            oa = None
            status = "Rejected"

        applications.append({

            "application_id": application_id,
            "student_id": student["student_id"],
            "drive_id": drive["drive_id"],
            "application_date":
                f"2026-{random.randint(8,10):02d}-{random.randint(1,28):02d}",
            "application_status": status,
            "oa_score": oa

        })

        application_id += 1

df = pd.DataFrame(applications)

# Force integers while keeping rejected students blank
df["oa_score"] = df["oa_score"].apply(
    lambda x: "" if pd.isna(x) else int(x)
)

df.to_csv(os.path.join(DATA_DIR, "applications.csv"), index=False)

print(df.head())
print("Applications:", len(df))