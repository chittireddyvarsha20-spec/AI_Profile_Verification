import pandas as pd
import random

rows = []

for i in range(800):

    # Genuine profiles
    if i < 300:
        name = round(random.uniform(0.8,1.0),2)
        job = round(random.uniform(0.7,1.0),2)
        company = round(random.uniform(0.7,1.0),2)
        presence = round(random.uniform(0.7,1.0),2)
        label = 0

    # Suspicious profiles
    elif i < 600:
        name = round(random.uniform(0.4,0.7),2)
        job = round(random.uniform(0.3,0.6),2)
        company = round(random.uniform(0.3,0.6),2)
        presence = round(random.uniform(0.3,0.6),2)
        label = 1

    # Fake profiles
    else:
        name = round(random.uniform(0.0,0.3),2)
        job = round(random.uniform(0.0,0.3),2)
        company = round(random.uniform(0.0,0.3),2)
        presence = round(random.uniform(0.0,0.3),2)
        label = 2

    rows.append([name,job,company,presence,label])

df = pd.DataFrame(rows, columns=[
    "name_match",
    "job_match",
    "company_match",
    "presence",
    "label"
])

df.to_csv("dataset.csv",index=False)

print("Improved dataset generated")