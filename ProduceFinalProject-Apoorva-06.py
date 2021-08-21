'''
Program:ProduceFinalProject-Apoorva-06.py
Author:Apoorva Arbooj
Purpose:Plot graph using the filters provided by user
Revisions: 
    01: Display products, dates and locations
    02: Create dictionary for graph plotting
    03: Write functions
    04: Create trace list
    05: Formatting the graph
    06: Added try catch to gracefully exit in case of error
'''

#%%
#FUNCTIONS#


def ftitle(title):
    print(f'\n{80*"-"}\n{f"{title:^80}"}\n{80*"-"}\n')

    
def printAvailableDates(dlist):
    for index,value in enumerate(dlist):
        if index % 4 == 0 and index != 0:0
            print()
        print(f'{f"<{index}>":<5}{datetime.strftime(value,"%Y-%m-%d"):<15}',end="")
        
    
def printAvailableProducts(plist):
    for index,value in enumerate(plist):
        if index % 3 == 0 and index != 0:
            print()
        print(f'{f"<{index}>":<5}{value:<20}',end="")

def avgPrice(priceList):
    len_plst=len(priceList)
    return 0 if len_plst == 0 else float(sum(priceList)/len_plst)

#%% Import the needed libraries

import csv
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go
#%%Print the formatted title of the program

#Formatted title
title='Commodity Final Project'
print(f'{80*"*"}\n{f"{title:^80}"}\n')

#%% (1)Read data from the csv file and store it in a list

data = []
csvfile = open('produce_csv.csv','r')
reader = csv.reader(csvfile)
for row in reader:  ###! main loop reads one row at a time
    if reader.line_num == 1: ###! get the location names from row 1
        locations = row[2:]  ###! slice to remove commodity and date
    else:
        for loc,value in zip(locations,row[2:]):  ###! iterate through locations and values
            row_num = len(data)     ###! index for the data row 
            data.append(row[:2])    ###! new data row: commodity and date
            data[row_num].append(loc)  ###! append location
            data[row_num].append(float(value.replace('$','')))     ###! append value
csvfile.close()

#%%

#Convert the date from string to datetime type
for d in data:
    d[1] = datetime.strptime(d[1],"%m/%d/%Y")

#Get the list of unique products from the data
uComList = sorted(list({d[0] for d in data }))

    
    #%% 

try:
    #(2)Display the available products
    # Get the products of choice from the user
    
    #Print out the list of available products to choose from
    ftitle("SELECT PRODUCTS BY NUMBER")
    printAvailableProducts(uComList)
    
    #Get the list of products the user wants
    userProdIndex = input('\nEnter product numbers separated by spaces: ').strip()

    #Convert the string to a list of integers
    userProdIndex = list(map(int,userProdIndex.split(' ')))
    
    #Make a list of selected products
    userProdSelected = [ uComList[i] for i in userProdIndex ]
    
    #Display the list of products selected by the user
    print(f'Selected products: {", ".join(userProdSelected)}')
    
    #%% (3)Display the available dates
    #Get the date range from the user
    
    #Create a list of dates only and sort it
    dates = sorted(list({d[1] for d in data }))
    
    #Display the available date range to choose from
    ftitle('SELECT DATE RANGE BY NUMBER ')
    printAvailableDates(dates)
    
    #Print the earliest date and latest date available
    print(f'\n{"Earliest Date":<13}: {datetime.strftime(dates[0],"%Y-%m-%d")}\n{"Latest Date":<13}: {datetime.strftime(dates[-1],"%Y-%m-%d")}')
    
    #Convert the string indexes entered by the user to integer and store it in a list
    userDateIndex = list(map(int,input('Enter start/end date numbers separated by a space: ').strip().split(' ')))
    
    #Check if only start and end date is entered by the user
    if len(userDateIndex) == 2:
        startDate = dates[userDateIndex[0]]
        endDate = dates[userDateIndex[1]]    
    else:
        #Tell the user that he has to enter only 2 dates for the range
        print(f'Please enter 2 dates (start and end) only.')
    
    #Display the entered start and end dates
    print(f'Dates from {datetime.strftime(startDate,"%Y-%m-%d")} to {datetime.strftime(endDate,"%Y-%m-%d")}')
    
    #%% (4)Display the available locations
    # Get the locations of choice from the user
    
    ftitle('SELECT LOCATIONS BY NUMBER')
    locations.sort()
    for index,value in enumerate(locations):
        print(f'{f"<{index}>":<5}{value:<20}')
    userLocIndex = list(map(int,input('Enter location numbers separated by spaces: ').strip().split(' ')))
    userLocSelected = [ locations[i] for i in userLocIndex ]
    print(f'Selected locations: {", ".join(userLocSelected)}')
    
    #%% (5)Select the records based on,
    # the products selected in the specified date range and for the required locations 
    selectedRecords =[d for d in data if d[0] in userProdSelected and startDate <= d[1] <= endDate and d[2] in userLocSelected]
    
    #Display the total records selected
    print(f'\n{len(selectedRecords)} records have been selected.')
    
    #%% (6)Create a dictionary using the selected records for plotting the graph

    #The selected locations will be the key of the dictionary
    selectedDict = { loc:[] for loc in userLocSelected}
     
    for loc in selectedDict:
        for prod in userProdSelected:
            #For every location-product pair,
            #Create a list of the prices
            #Calculate the average of the prices
            #Append the average price (value) to the location (key)
            selectedDict[loc].append(avgPrice([r[3] for r in selectedRecords if r[0] == prod and r[2] == loc]))
        
    #%% (7)Plotting the graph
    
    #Data for plotting graph
    trace = []
    for loc,avgPLst in selectedDict.items():
        trace.append(go.Bar(x=userProdSelected,y=avgPLst,name=loc))

    #Formatting the graph
    graph_title = 'Produce Prices from '+datetime.strftime(startDate,"%Y-%m-%d")+' through '+datetime.strftime(endDate,"%Y-%m-%d")
    layout = go.Layout(barmode='group',
                       title=dict(text='<b>'+graph_title+'</b>', x=0.5, xanchor="center"),
                       xaxis=dict(title='Product'),
                       yaxis=dict(title='Average Price',tickprefix="$",tickformat=".2f"),
                       font=dict(family="Lucida Console",size=18,color="#233459")
                   )
    
    #Plot the graph and save it in a html file
    fig = go.Figure(data=trace, layout=layout)
    py.plot(fig, filename='ProduceFinalProject-Apoorva-Graph.html')
    
    #%%   
    
except ValueError:
    print('\nPlease enter integers only.')
except IndexError:
    print('\nPlease select from the available list.')
except:
    print('\nPlease enter values as instructed.')
    


