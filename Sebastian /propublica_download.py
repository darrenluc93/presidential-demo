#Database libraries
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import Session 
from sqlalchemy.ext.declarative import declarative_base

#DataFrame libraries
import pandas as pd

#Declares the type of base we want
Base = declarative_base()

#Creates the engine of the database.
engine = create_engine("sqlite:///Election2020Data.sqlite")

#Stablishes the session in the engine.
session = Session(engine)

#Define the class. 
class donor(Base):
    __tablename__ = "2020Donors"
    Record_id = Column(Integer, primary_key = True)
    Flag_Orgind = Column(String, nullable = True)
    Org_name = Column(String, nullable = True)
    Last_Name = Column(String, nullable = True)
    First_Name = Column(String, nullable = True)
    Middle_Name = Column(String, nullable = True)
    Prefix = Column(String, nullable = True)
    Suffix = Column(String, nullable = True)
    Address_One = Column(String, nullable = True)
    Address_Two = Column(String, nullable = True)
    City = Column(String, nullable = True)
    State = Column(String, nullable = True)
    Zip = Column(String, nullable = True)
    Employer = Column(String, nullable = True)
    Occupation = Column(String, nullable = True)
    Amount = Column(Float, nullable = True)
    Date = Column(Date, nullable = True)
    Aggregate_Amount = Column(Float, nullable = True)
    Cycle = Column(Integer, nullable = True)
    Campaign = Column(String, nullable = True)

#Creates the table
Base.metadata.create_all(engine)

#Lists to loop
list_States = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
          
list_Info = ['q1_2019','q2_2019','q3_2019','q4_2019', 'm1_2020','m2_2020','m3_2020','m4_2020','m5_2020','m6_2020','m7_2020','m8_2020']

for state in list_States:
    print(state)

    for info in list_Info:
        print(info)

        #Foor loop builds the https address where the csv is stored and then pandas opens the data as DataFrame
        temp_df = pd.read_csv(f"https://pp-projects-static.s3.amazonaws.com/itemizer/president/contributions_{info}_{state}.csv")

        for index, row in temp_df.iterrows():

            #Loops each line and adds it to the database.
            session.add(donor(
                            Flag_Orgind = row['flag_orgind'],
                            Org_name = row['org_name'],
                            Last_Name = row['last_name'],
                            First_Name = row['first_name'],
                            Middle_Name = row['middle_name'],
                            Prefix = row['prefix'],
                            Suffix = row['suffix'],
                            Address_One = row['address_one'],
                            Address_Two = row['address_two'],
                            City = row['city'],
                            State = row['state'],
                            Zip = row['zip'],
                            Employer = row['employer'],
                            Occupation = row['occupation'],
                            Amount = row['amount'],
                            Date = pd.to_datetime(row['date']),
                            Aggregate_Amount = row['aggregate_amount'],
                            Cycle = row['cycle'],
                            Campaign = row['committee_name']
                            ))
        #Commits changes                   
        session.commit()

#Disposes engine.
engine.dispose()

print('Done')