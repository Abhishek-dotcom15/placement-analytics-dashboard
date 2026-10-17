import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

apps = pd.read_csv(os.path.join(DATA_DIR, "applications.csv"))
drives = pd.read_csv(os.path.join(DATA_DIR, "placement_drives.csv"))

offers = []

offer_id=1

for _, app in apps.iterrows():

    if app["application_status"] not in ["Offered","Accepted"]:
        continue

    drive = drives[
        drives["drive_id"]==app["drive_id"]
    ].iloc[0]

    offers.append({

        "offer_id":offer_id,

        "application_id":app["application_id"],

        "offered_ctc":drive["ctc"],

        "offer_date":
        f"2026-09-{random.randint(1,30):02d}",

        "accepted":
        app["application_status"]=="Accepted"

    })

    offer_id+=1

df=pd.DataFrame(offers)

df.to_csv(os.path.join(DATA_DIR, "offers.csv"), index=False)

print(df.head())
print("Offers:",len(df))
