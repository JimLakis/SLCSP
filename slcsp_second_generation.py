# Python v3.6


import numpy as np
import pandas as pd


def creating_dataframes():
    ''' Creating Panda DataFramse (df) from the csv files. '''
    zips = pd.read_csv('zips.csv', delimiter=',', dtype={'zipcode': np.unicode_, 'rate_area': np.unicode_})
    plans = pd.read_csv('plans.csv', delimiter=',', dtype={'rate_area': np.unicode_})
    slcsp = pd.read_csv('slcsp.csv', delimiter=',', dtype={'zipcode': np.unicode_})
    # zips columns: [zipcode, state, county_code, name, rate_area]
    # plans columns: [plan_id, state, metal_level, rate, rate_area]
    return zips, plans, slcsp


def cleanup_zips(zips, slcsp):
    ''' Reducing the number of records in the zips df to relevant records. '''   
    def only_slcsp_zipcodes(zips, slcsp):
        ''' Only carrying forward records in the zips df where zipcode values match those found in the target slcsp df. '''
        zips_in_slcsp = zips[zips.zipcode.isin(slcsp.zipcode)]
        del zips
        return zips_in_slcsp

    def only_multiple_zipcodes(zips_in_slcsp):
        ''' Only carrying forward records in the zips df where zipcode values have more than one entry.
            First step is to create a df with only single entries of the zipcodes.
            The second step utilizes the new df of single entries to exclude those records from the creation of another df containing only zipcodes with more than one entry. '''
        zips_single_zipcodes = zips_in_slcsp.drop_duplicates(subset = 'zipcode', keep = False)
        zips_multiple_zipcodes = zips_in_slcsp[~zips_in_slcsp.zipcode.isin(zips_single_zipcodes.zipcode)]
        del zips_single_zipcodes
        return zips_multiple_zipcodes

    zips_in_slcsp = only_slcsp_zipcodes(zips, slcsp)
    zips_multiple_zipcodes = only_multiple_zipcodes(zips_in_slcsp)
    return zips_multiple_zipcodes


def cleanup_plans(plans):
    ''' Reducing the number of records in the plans df to relevant records.
        Only records where the metal_level is "Silver" is carried forward. '''
    plans_silver = plans[plans.metal_level == "Silver"]
    return plans_silver


def concatenate_within_zips_plans(zips, plans):
    ''' Concatenate the state and the rate_area columns in the zips and plans dfs. '''
    def concatenate_rate_area_state(zips, plans):
        ''' Concatenate the state and the rate_area columns in the zips and plans dfs. '''
        zips['state_rate_area'] = zips['state'] + ' ' + zips['rate_area']
        plans['state_rate_area'] = plans['state'] + ' ' + plans['rate_area']
        return zips, plans

    def drop_original_rate_area_state(zips, plans):
        ''' Dropping the needless state and rate_area columns. '''
        zips.drop(columns = ['state', 'rate_area'], inplace = True)
        plans.drop(columns = ['state', 'rate_area'], inplace = True)
        return zips, plans

    zips, plans = concatenate_rate_area_state(zips, plans)
    zips, plans = drop_original_rate_area_state(zips, plans)
    return zips, plans


def main():
    zips, plans, slcsp = creating_dataframes()
    zips = cleanup_zips(zips, slcsp)
    slcsp = cleanup_plans(plans)
    zips, plans = concatenate_within_zips_plans(zips, plans)
    # To be continued...


if __name__ == '__main__':
    main()