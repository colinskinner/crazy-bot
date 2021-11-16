import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://en.wikipedia.org/wiki/List_of_jet_airliners"

response = requests.get(URL)  # page

soup = BeautifulSoup(response.text, 'html.parser')  # scraped

tables = soup.find_all('table', {"class":"wikitable sortable"})  #all tables from page
total = [] # array to contain plane objects

for table in tables:

    rows = table.find_all('tr')  #each row in plane

    columns = [v.text.replace('\n', "") for v in rows[0].find_all('th')]  #finds headers, puts them into columns list
    df = pd.DataFrame(columns=columns)  #empty column data structure

    for i in range(1, len(rows)):
        tds = rows[i].find_all('td')  #each table cell

        values = [td.text.replace('\n', "") for td in tds]  #adds table cell to a values array

        df = df.append(pd.Series(values, index=columns),ignore_index=True)  #puts values array into df datastructure under respective column

    total.append(df)  #add df to total array
final = pd.concat(total, ignore_index=True)  #adds all of total to a final data structure


#column formating - combining columns with *slightly* different titles
final["Origin"] = final["Origin"].astype(str).replace('nan', "") + final["Country"].astype(str).replace('nan', "")
final["Engines"] = final["Engines[a]"].astype(str).replace('nan', "") + final["Engines[c]"].astype(str).replace('nan', "") + final["Engines[f]"].astype(str).replace('nan', "")
final["In Service"] = final["In Service [1][b]"].astype(str).replace('nan', "") + final["In Service (2020)[1][d]"].astype(str).replace('nan', "")
final = final.drop(["Origin", "Country", "Engines[a]", "Engines[c]", "Engines[f]","In Service [1][b]","In Service (2020)[1][d]"], axis=1)

#row formatting - deleting cancelled or only planned planes
final = final[~final["First Flight"].str.contains("planned")]
final = final[~final["First Flight"].str.contains("cancelled")]
final = final[~final["Airline service entry"].str.contains("planned")]
final = final[~final["Airline service entry"].str.contains("cancelled")]

#export to csv file
final.to_csv(r'planes.csv')
