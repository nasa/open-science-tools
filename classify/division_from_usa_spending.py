import requests
import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from time import sleep


# --- Example Usage ---
if __name__ == "__main__":

    div_dict = {}
    div_dict['STMD, Space Tech'] = 'STMD'
    div_dict['Aeronautics'] = 'ARD'
    div_dict['Space Operations'] = 'SOMD'
    div_dict['Exploration Systems Development Mission Directorate (ESDMD)'] = 'ESDMD'
    div_dict['OSTEM'] = 'OSTEM'
    div_dict['SMD'] = ''
    div_dict[None] = ''


    pubs =  pd.read_csv('nasa_publications_division.csv')
   
    total = 0
    for index, gr, div in zip(pubs.index, pubs['Grant ID'], pubs['Division']):
        if div is np.nan:
           sleep(0.1)
           if type(gr) == float:
              gr=str(gr)
           d = ''
           for g in gr.split(';'):
               if g.count('NSSC') or g.count('NNX'):
                  target_award_number = g.strip()
                  try:
                      r = requests.get(f'https://api.usaspending.gov/api/v2/awards/ASST_NON_{target_award_number}_080')
                  except Exception as e:
                      print(e)
                      print(total)
                      print(index)
                      print("Fail")
                      pubs.to_csv("temp_fail6.csv")
                      exit()
                  if r.status_code == 200:
                     j = r.json()
                     d = j['cfda_info'][0]['cfda_popular_name']
                     try:
                        d = div_dict[d]
                     except:
                        d = ''
                     if d:
                        pubs.at[index, 'Division'] = d 
                        total += 1

    output = pubs.loc[~pubs['Division'].isna()]
    output.to_csv('nasa_publications_division_spending.csv')
