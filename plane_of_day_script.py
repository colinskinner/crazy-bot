import csv

plane_rows = []

with open('planes.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for p in spamreader:
        for i in p:
            i = i.replace(',','')
        plane_rows.append(p)
        
plane_rows.pop(0)
Type = 1
FirstFlight = 2
AirlineServiceEntry = 3
EndOfProduction = 4
NumberBuilt = 5
YearRetired = 6
Engines = 7
InService = 8


#takes in row (plane) and outputs what type of plane it is
def type_of_plane(row, speech=False):
    if "discontinued" in row[EndOfProduction].lower():
        if speech:
            print(row[Type] + " is discontinued.")
        return "Discontinued"
    elif "to be introduced" in row[EndOfProduction].lower():
        if speech:
            print(row[Type] + " is to be introduced.")
        return "To be Introduced"
    elif row[YearRetired].lower() != '':
        if speech:
            print(row[Type] + " is historical.")
        return "Historical"

    elif "production" in row[EndOfProduction].lower():
        if speech:
            print(row[Type] + " is Currently in Production.")
        return "Currently in Production"
    else:
        if speech:
            print(row[Type] + " is Out in Production.")
        return "Out of Production"
        
for p in plane_rows:
    type_of_plane(p,True)

#Currently in Production
#Out of Production
#Historical