# Python v3.6


import numpy as np
import pandas as pd


def creating_dataframes():
    ''' Loading csv files into Pandas dataframes (df) '''
    zips = pd.read_csv('zips.csv', delimiter=',', dtype={'zipcode': np.unicode_})
    plans = pd.read_csv('plans.csv', delimiter=',')
    slcsp = pd.read_csv('slcsp.csv', delimiter=',', dtype={'zipcode': np.unicode_})
    print("Intital dataframes")
    print(f"Zips records: {np.shape(zips)[0]}")
    print(f"Plans records: {np.shape(plans)[0]}")
    print(f"SLCSP records: {np.shape(slcsp)[0]}\n")
    # zips columns: [zipcode, state, county_code, name, rate_area]
    # plans columns: [plan_id, state, metal_level, rate, rate_area]
    return zips, plans, slcsp

def zips_in_target(zips, slcsp):
    ''' Carrying forward only the zipcodes found in the slcsp df to be present in the zips df.
        A series containing a boolean mask on the zipcode column in the zips df based on whether they are present in the final slcsp df is created.
        That boolean mask is then applied back onto the zips df itself.'''
    zips_verified = zips[zips.zipcode.isin(slcsp.zipcode)]
    print(f"Zipcode exclusion. Only zipcodes in final SLCSP carry forward in zips dataframe.\nZips records: {np.shape(zips_verified)[0]}\n")
    return zips_verified

def filter_for_silver(plans):
    ''' Carrying forward only the silver metal level plans in the plans df. 
        A series containing a boolean mask on the metal_level column in the plans df evaluating whether the metal level plan is 'Silver' is created.
        That boolean mask is then applied back onto the plans df itself.'''
    plans_silver = plans[plans.metal_level == "Silver"]
    print(f"Filter for 'Silver' plans. Only silver plans carry forward in plans dataframe.\nPlans records: {np.shape(plans_silver)[0]}")
    return plans_silver
    

def main():
    print("SLCSP problem - cleaning data, only.\n")
    zips, plans, slcsp = creating_dataframes()
    zips_verified = zips_in_target(zips, slcsp)
    plans_silver = filter_for_silver(plans)

if __name__ == '__main__':
    main()
    
