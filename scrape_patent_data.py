# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

# Set the URL you want to webscrape from
url_template = 'https://www.uspto.gov/web/offices/ac/ido/oeip/taf/st_co_'
urls = []
#for year in range(11,12):
for year in range(10,20):
    urls.append(url_template + str(year) + ".htm")



def parse_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    #soup = BeautifulSoup(response)
    return [(table['summary'],parse_html_table(table))\
            for table in soup.find_all('table')]  

def parse_html_table(table):
    n_columns = 0
    n_rows=0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):
        
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)
                
        # Handle column names if we find them
        th_tags = row.find_all('th') 
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,
                      index= range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
            
    # Convert to float if possible
    for col in df:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass
    
    return df


state_table = {}
for next_url in urls:
    data = parse_url(next_url)
    #print(data[0][1])
    #print(data[0][1]['Utility'])
    #print(data[0][1].to_numpy())
    onlyStates = 0
    for row in data[0][1].to_numpy():
        if onlyStates < 50 and len(str(row[1]).strip()) < 3:
            #print(str(row[1]).strip() + " " + str(row[7]).strip())
            state_table.setdefault(str(row[1]).strip(), []).append(str(row[7]).strip())
        onlyStates += 1
    #for row in data[0][1].iterrows():
    #    print(data)
#print(state_table)
    
print(".", end=",")
for key in state_table:
    print(key, end=",")
print()
for year in range(2011, 2020):
    print(str(year), end=",")
    for key in state_table:
        print(state_table[key][year - 2011], end=",")
    print()

        
            


