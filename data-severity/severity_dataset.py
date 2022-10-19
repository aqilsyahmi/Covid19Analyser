import urllib.request as url
import pandas as pd
import matplotlib.pyplot as mpl
import sys
import os
from pathlib import Path
path = Path(__file__).parent


# Tuple(csvFilename,dateColumnName,location)
casesBySeverity = (str(path)+"/deaths-and-active-cases-in-icu-requiring-oxygen-supplementation-or-hospitalised.csv",
                   "day_of_as_of_date","%Y/%m/%d",
                   "NA")
casesTotal = (str(path)+"/owid-covid-data.csv",
              "date",
              "%Y/%m/%d",
              "Singapore")


# input: dataframe
# return: reconstructed df
def restructureDataFrame(data):
    currentSevereCases = data.groupby(['day_of_as_of_date', 'clinical_status']).sum()
    pivotTable = pd.pivot_table(currentSevereCases, values="count_of_case", index=["day_of_as_of_date"], columns=["clinical_status"])
#     pivotTable["TotalSevereCases"] = pivotTable.sum(axis=1)
    return pivotTable


# input: csv file
# return: df sorted by date
# Read csv file and filter out based on country.
# Convert date to correct format and sort
def readCsv(dSet):
    dataSet = pd.read_csv(dSet[0])
    if dSet[3] == "Singapore":
        dataSet = dataSet[dataSet.location.eq("Singapore")]
    dataSet[dSet[1]] = pd.to_datetime(dataSet[dSet[1]], format=dSet[2]).dt.strftime("%Y-%m-%d")
    dfByDate = dataSet.sort_values(by=[dSet[1]])
    return dfByDate


# input: dataframe(index=datetime),month(int),year(int)
# output: sortedDf
# To sort by a specific time frame, either by month or by year
def sortByDate(dataFrame, month, year):
    if month == 0:
        startdate = pd.to_datetime("%s-01-01"%year).date()
        enddate = pd.to_datetime("%s-12-01"%year).date()
        enddate = pd.Period(enddate, freq='M').end_time.date()
        dataFrame = dataFrame.loc[startdate:enddate]
        dataFrame = dataFrame.groupby([lambda x: x.year, lambda x: x.month]).sum()
    else:
        startdate = pd.to_datetime('%s-%s-01'%(year, month)).date()
        enddate = pd.to_datetime('%s-%s-01'%(year, month)).date()
        enddate = pd.Period(enddate, freq='M').end_time.date()
        dataFrame = dataFrame.loc[startdate:enddate]
    return dataFrame


# input: dataframe, column that divides, column that divided, new column that store the value
# return: dataframe
# To recalculate the rate, as sortByDate function will add up all the rate when sort by year
def reCalculateRate(dataFrame, total, columns, newColumn):
    df = dataFrame.copy()
    columnTotal = df[columns[0]]
    for column in columns[1:len(columns)]:
        columnTotal += df[column]
    dataFrame[newColumn] = (columnTotal/dataFrame[total])*100
    return dataFrame


# input: dataframe, new Column Name, target Column name
# return: Null
# calculate the Daily Severe Cases from current severe cases
def calculateDailySevereCases(dataframe, newColumn, targetColumn):
    dataframe[newColumn] = dataframe[targetColumn].diff()
    dataframe[newColumn] = dataframe.apply(lambda x: x[newColumn] if x[newColumn]>0 else 0, axis=1) 

    
# input: df1, df2
# Return: merged Df
# Return a merged dataframe
def merge2Table(df1, df2):
    mergeTable = df1.join(df2)
#     mergeTable = dailyCasesDF.join(currentSevereCasesDF)
    mergeTable.index = pd.to_datetime(mergeTable.index)
    mergeTable.index = mergeTable.index.date
    return mergeTable


# input: data frame
# return: data frame
# get the severity rate by add up different columns and divide by the total daily cases
def calculateSeverityRate(mergeTable):
    mergeTable.columns = mergeTable.columns.str.replace(' ', '')
    calculateDailySevereCases(mergeTable, "DailyHospitalised", "Hospitalised")
    calculateDailySevereCases(mergeTable, "DailyICU", "InIntensiveCareUnit")
    calculateDailySevereCases(mergeTable, "DailyOxygen", "RequiresOxygenSupplementation")
    totalSevere = mergeTable["DailyICU"] + mergeTable["DailyOxygen"]
    mergeTable["SeverityRate(%)"] = (totalSevere/mergeTable["DailyCases"])*100
    mergeTable = mergeTable.round(2)
    return mergeTable


# input: dataFrame
# return: null
# Plot a chart for testing purpose
def plotGraph(dataFrame):
    fig, ax1 = mpl.subplots()
    ax1.bar(dataFrame[['DailyICU', 'DailyOxygen']]) #.plot(kind='barh', title="Total Hospitalisation", legend=True, fontsize=9, stacked=True)
    ax1.set_xlabel("Cases", fontsize=12)
    ax1.set_ylabel("Date", fontsize=12)
    # mpl.show()


# pd.set_option("display.max_rows", None, "display.max_columns", None)
dailyCasesDF = readCsv(casesTotal)[['date', 'new_cases']].set_index('date').rename(columns={"new_cases": "DailyCases"})
currentSevereCasesDF = restructureDataFrame(readCsv(casesBySeverity))
mergeTable = merge2Table(dailyCasesDF, currentSevereCasesDF)

# Import this file call the variable below to get the complete table
severityRateDF = calculateSeverityRate(mergeTable)

# -----------------------------------------------------------------------
# BELOW ONE IS FOR TESTING PURPOSE
# plotGraph(sortByDate(severityRateDF,10,2021))
