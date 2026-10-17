import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

companies = [

("Google","Technology","Product","California","https://google.com"),
("Microsoft","Technology","Product","Washington","https://microsoft.com"),
("Amazon","Technology","Product","Seattle","https://amazon.com"),
("Adobe","Technology","Product","California","https://adobe.com"),
("Apple","Technology","Product","California","https://apple.com"),
("Meta","Technology","Product","California","https://meta.com"),
("NVIDIA","Technology","Product","California","https://nvidia.com"),
("Oracle","Technology","Product","Texas","https://oracle.com"),
("Salesforce","Technology","Product","California","https://salesforce.com"),
("Intel","Technology","Product","California","https://intel.com"),

("Accenture","Consulting","Service","Dublin","https://accenture.com"),
("Deloitte","Consulting","Service","London","https://deloitte.com"),
("PwC","Consulting","Service","London","https://pwc.com"),
("EY","Consulting","Service","London","https://ey.com"),
("KPMG","Consulting","Service","London","https://kpmg.com"),
("ZS Associates","Consulting","Service","Illinois","https://zs.com"),
("McKinsey","Consulting","Service","New York","https://mckinsey.com"),
("BCG","Consulting","Service","Boston","https://bcg.com"),
("Bain","Consulting","Service","Boston","https://bain.com"),

("Goldman Sachs","Finance","Service","New York","https://goldmansachs.com"),
("JPMorgan Chase","Finance","Service","New York","https://jpmorgan.com"),
("American Express","Finance","Service","New York","https://americanexpress.com"),
("Morgan Stanley","Finance","Service","New York","https://morganstanley.com"),

("Flipkart","E-Commerce","Product","Bangalore","https://flipkart.com"),
("Meesho","E-Commerce","Product","Bangalore","https://meesho.com"),
("Zepto","E-Commerce","Product","Mumbai","https://zepto.com"),
("Blinkit","E-Commerce","Product","Gurgaon","https://blinkit.com"),
("Swiggy","E-Commerce","Product","Bangalore","https://swiggy.com"),
("Zomato","E-Commerce","Product","Gurgaon","https://zomato.com"),

("Samsung","Electronics","Product","Seoul","https://samsung.com"),
("Qualcomm","Electronics","Product","California","https://qualcomm.com"),
("Texas Instruments","Electronics","Product","Texas","https://ti.com"),
("NXP","Electronics","Product","Netherlands","https://nxp.com"),
("MediaTek","Electronics","Product","Taiwan","https://mediatek.com"),

("TCS","IT Services","Service","Mumbai","https://tcs.com"),
("Infosys","IT Services","Service","Bangalore","https://infosys.com"),
("Wipro","IT Services","Service","Bangalore","https://wipro.com"),
("HCL","IT Services","Service","Noida","https://hcltech.com"),
("Tech Mahindra","IT Services","Service","Pune","https://techmahindra.com")
]

rows=[]

company_id=1

while len(rows)<150:

    c=random.choice(companies)

    rows.append({

        "company_id":company_id,
        "company_name":c[0],
        "industry":c[1],
        "company_type":c[2],
        "headquarters":c[3],
        "website":c[4],
        "returning_company":random.choice([True,False])

    })

    company_id+=1

df=pd.DataFrame(rows)

df.to_csv(os.path.join(DATA_DIR, "companies.csv"), index=False)

print(df.head())

print("Companies Generated:",len(df))