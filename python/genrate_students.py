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

    # blocked students cannot participate
    if student["placement_status"] != "Eligible":
        continue

    # check every placement drive
    for _, drive in drives.iterrows():

        # CGPA eligibility
        if student["cgpa"] < drive["minimum_cgpa"]:
            continue

        # probability that student applies
        if random.random() > 0.60:
            continue

        # ---------- Resume Shortlisting ----------

        shortlist_score = (
            0.45 * student["resume_score"]
            + 0.35 * student["cgpa"] * 10
            + 0.20 * student["coding_score"]
        )

        if shortlist_score >= 82:

            status = "Resume Shortlisted"

            oa_score = max(
                0,
                min(
                    100,
                    int(student["coding_score"] + random.randint(-10, 10))
                )
            )

            if oa_score >= 70:

                status = "OA Cleared"

                if random.random() < 0.75:

                    status = "Interviewing"

                    interview_score = (
                        student["communication_score"]
                        + random.randint(-10,10)
                    )

                    if interview_score >= 70:

                        status = "Offered"

                        if random.random() < 0.85:

                            status = "Accepted"

            else:

                status = "Rejected"

        else:

            oa_score = None
            status = "Rejected"

        applications.append({

            "application_id": application_id,

            "student_id": student["student_id"],

            "drive_id": drive["drive_id"],

            "application_date":
                f"2026-08-{random.randint(1,30):02d}",

            "application_status": status,

            "oa_score": oa_score

        })

        application_id += 1

applications = pd.DataFrame(applications)

applications.to_csv(
    os.path.join(DATA_DIR, "applications.csv"),
    index=False
)

print(f"{len(applications)} applications generated.")