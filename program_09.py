#!/bin/env python
"""
Les Warren warre112
Created 03/24/2020
Lab09, DataQualtyChecking, ABE65100

This program is designed to quality data check for four different error types
(No Data Value, Gross Errors, Swapping misplaced values, and Range Check). It also 
plots original data compared to QC data and exports findings as a .txt file(s)

"""
import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data", "2.Gross Error", "3. Swapped", "4.Range"], columns=colNames[1:]) ##added row names 2-4
     
    return( DataDF, ReplacedValuesDF )
    
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    
    for i in range (0,len(DataDF)-1):
        for j in range(0,3):
            if DataDF.iloc[i,j] == -999: #removing any values =-999
                   DataDF.iloc[i,j]= np.nan
   
    ReplacedValuesDF.iloc[0,0]=DataDF['Precip'].isna().sum()
    ReplacedValuesDF.iloc[0,1]=DataDF['Max Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,2]=DataDF['Min Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,3]=DataDF['Wind Speed'].isna().sum()

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
#Precipiation 
    for i in range (0,len(DataDF)-1):
           if (DataDF['Precip'].iloc[i]<0) or (DataDF['Precip'].iloc[i]>25): #Replacing values out of 0-25 range with nan
               DataDF['Precip'].iloc[i]= np.nan
#Temperature
    for i in range (0,len(DataDF)-1): #replacing values outside of -25 to 35 range with nan
           if DataDF['Max Temp'].iloc[i]< (-25) or DataDF['Max Temp'].iloc[i] >35:
               DataDF['Max Temp'].iloc[i]= np.nan
    
    for i in range (0,len(DataDF)-1): #replacing values outside of -25 to 35 range with nan
           if DataDF['Min Temp'].iloc[i]< (-25) or DataDF['Min Temp'].iloc[i] >35:
               DataDF['Min Temp'].iloc[i]= np.nan
#Wind Speed      
    for i in range (0,len(DataDF)-1):
           if (DataDF['Wind Speed'].iloc[i]<0) or (DataDF['Wind Speed'].iloc[i]>10):  #replacing values outside of 0 to 10 range with nan
               DataDF['Wind Speed'].iloc[i]= np.nan
               
    ReplacedValuesDF.iloc[1,0]=DataDF['Precip'].isna().sum()-ReplacedValuesDF.iloc[0,0]
    ReplacedValuesDF.iloc[1,1]=DataDF['Max Temp'].isna().sum()-ReplacedValuesDF.iloc[0,1]
    ReplacedValuesDF.iloc[1,2]=DataDF['Min Temp'].isna().sum()-ReplacedValuesDF.iloc[0,2]
    ReplacedValuesDF.iloc[1,3]=DataDF['Wind Speed'].isna().sum()-ReplacedValuesDF.iloc[0,3]
               
    return(DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    ReplacedValuesDF.iloc[2,1]=(DataDF['Min Temp'] > DataDF['Max Temp']).sum() #How many need swapping 
    ReplacedValuesDF.iloc[2,2]=(DataDF['Min Temp'] > DataDF['Max Temp']).sum()
    for i in range(0,len(DataDF)-1):
        if DataDF['Min Temp'].iloc[i] > DataDF['Max Temp'].iloc[i]: #if Tmin > Tmax
            hold = DataDF['Max Temp'].iloc[i] 
            DataDF['Max Temp'].iloc[i] = DataDF['Min Temp'].iloc[i] #move Tmax value to the Tmin value
            DataDF['Min Temp'].iloc[i] = hold #move Tmin value with the old Tmax value (that was in the placeholder)
    
    return( DataDF, ReplacedValuesDF )
      

    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    ReplacedValuesDF.iloc[3,1]=(DataDF['Max Temp'] - DataDF['Min Temp'] > 25).sum() #number of days the temperature range was >25
    ReplacedValuesDF.iloc[3,2]=(DataDF['Max Temp'] - DataDF['Min Temp'] > 25).sum() 
    
    for i in range(0,len(DataDF)-1):
        if DataDF['Max Temp'].iloc[i] - DataDF['Min Temp'].iloc[i] > 25: #difference between tmax & tmin > 25
            DataDF['Max Temp'].iloc[i] = np.nan #replace with nan
            DataDF['Min Temp'].iloc[i] = np.nan #replace  with nan

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    

#Read Data
ReadData('DataQualityChecking.txt')

#Create copy of raw data
colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
Raw = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
Raw = Raw.set_index('Date')


#Plot Data
import matplotlib.pyplot as plt
##Precipitation 
plt.plot(DataDF.index, Raw['Precip'],'b*', label='Raw Data')
plt.plot(DataDF.index, DataDF['Precip'],'r*', label='After Data Quality')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.legend()
plt.savefig('Precipitation.png')


##Max Temp
plt.plot(DataDF.index, Raw['Max Temp'],'b*', label='Raw Data')
plt.plot(DataDF.index, DataDF['Max Temp'],'r*', label='After Data Quality')
plt.xlabel('Date')
plt.ylabel('Maximum Temperature (C)')
plt.legend()
plt.savefig('MaxTemp.png')


##Min Temp
plt.plot(DataDF.index, Raw['Min Temp'],'b*', label='Raw Data')
plt.plot(DataDF.index, DataDF['Min Temp'],'r*', label='After Data Quality')
plt.xlabel('Date')
plt.ylabel('Minimum Temperature (C)')
plt.legend()
plt.savefig('MinTemp.png')


##Wind Speed
plt.plot(DataDF.index, Raw['Wind Speed'],'b*', label='Raw Data')
plt.plot(DataDF.index, DataDF['Wind Speed'],'r*', label='After Data Quality')
plt.xlabel('Date')
plt.ylabel('Wind Speed (m/s)')
plt.legend()
plt.savefig('WindSpeed.png')


#Wrtie Data to TAB Deliniated Files
DataDF.to_csv('After_DataQuality.txt', sep='\t', index=True)

ReplacedValuesDF.to_csv('ReplacedValues.txt', sep='\t', index=True)