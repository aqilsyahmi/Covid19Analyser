import sys
import matplotlib.pyplot as plt
import covidAnalyser as ca
import datetime as dt
import pandas as pd
from matplotlib.widgets import CheckButtons
from pathlib import Path

path = Path(__file__).parent

# Benny's Sort Date Method
# If month is zero then filter by year
# If month has value then show all month in that year
def sortByDate(dataFrame,month,year):
    try:
        if month == 0:
            startdate = pd.to_datetime("%s-01-1"%year).date()
            enddate = pd.to_datetime("%s-12-1"%year).date()
            enddate = pd.Period(enddate,freq='M').end_time.date()
            dataFrame = dataFrame.loc[startdate:enddate]
            dataFrame = dataFrame.groupby([lambda x: x.year, lambda x: x.month]).sum()
        else:
            startdate = pd.to_datetime('%s-%s-01'%(year, month)).date()
            enddate = pd.to_datetime('%s-%s-01'%(year, month)).date()
            enddate = pd.Period(enddate,freq='M').end_time.date()
            dataFrame = dataFrame.loc[startdate:enddate]   
    except:
        print("Please Input correct year")
        sys.exit()
    return dataFrame

# Input:
#   dateSeries Series to index
#   firstSeries to concat
#   secondSeries to concat
# Output: An indexed Series with a dataframe comprising of 2 concat series
def indexDataFrameByDateAndConcatTwoSeries(dateSeries, firstSeries, secondSeries):
    DailyConfirmedAndDischargedDataFrame = pd.concat([dateSeriesDate, dataSeriesDailyConfirmed, dataSeriesDailyDischarged,dataSeriesRecoveryRate['Daily Recovery']], axis=1)
    DailyConfirmedAndDischargedDataFrame = DailyConfirmedAndDischargedDataFrame.set_index('Date')
    DailyConfirmedAndDischargedDataFrame.index = pd.to_datetime(DailyConfirmedAndDischargedDataFrame.index)
    DailyConfirmedAndDischargedDataFrame.index = DailyConfirmedAndDischargedDataFrame.index.date
#     indexedByDateTimeDataFrame = sortByDate(DailyConfirmedAndDischargedDataFrame, 0, 2021)
    return DailyConfirmedAndDischargedDataFrame


# Reads a csv file and store the returned dataframe
file = str(path)+'/191021.csv'
csvFile = ca.readCsv(file)

# Get the list of Dates (as a Series) for the x-axis
dateSeriesDate = ca.readCsvOfAColumnFromRowXToRowY(csvFile, 'Date', 2, 635)

# Line 1 Daily Confirm Cases
dataSeriesDailyConfirmed = ca.readCsvOfAColumnFromRowXToRowY(csvFile, 'Daily Confirmed', 2, 635)

# Line 2 Daily Discharged Cases
dataSeriesDailyDischarged = ca.readCsvOfAColumnFromRowXToRowY(csvFile, 'Daily Discharged', 2, 635)

# Line 3 Daily Recovery Rate (Calculated for Analysis)
dataSeriesRecoveryRate = ca.readTwoColumnOfCsvFromRowXToRowY(csvFile, 'Daily Confirmed', 'Daily Discharged', 2, 635)
dataSeriesRecoveryRate['Daily Recovery'] = dataSeriesRecoveryRate['Daily Discharged'] - dataSeriesRecoveryRate['Daily Confirmed']
dataSeriesRecoveryRate['Daily Recovery'] = dataSeriesRecoveryRate.apply(lambda x:x['Daily Recovery'] if x['Daily Recovery'] >=0 else 0,axis=1)

# ---------------------------------------------------------------------------------------------------------------------------
# BELOW ONE IS FOR SELF TESTING PURPOSE
# fig, ax = plt.subplots()

mergeDataFrame=indexDataFrameByDateAndConcatTwoSeries(dateSeriesDate, dataSeriesDailyConfirmed, dataSeriesDailyDischarged)
# print(indexDataFrameByDateAndConcatTwoSeries(dateSeriesDate, dataSeriesDailyConfirmed, dataSeriesDailyDischarged))

# plt.xticks(rotation=45)
#
# # Plotting the 3 lines
# p1, = ax.plot(dateSeriesDate, dataSeriesDailyConfirmed, color='red', label='Confirmed')
# p2, = ax.plot(dateSeriesDate, dataSeriesDailyDischarged, color='blue', label='Discharged', visible=True)
# p3, = ax.plot(dateSeriesDate, dataSeriesRecoveryRate['Daily Recovery'], color='green', label='Recovered', visible=True)
# lines = [p1, p2, p3]
#
# # Formatting the x-axis of datetime as YYYY-MM-DD
# [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dateSeriesDate.values]
# plt.gca().set_xbound(dateSeriesDate.values[0], dateSeriesDate.values[-1])
# plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))
#
#
# # This shifts the WHOLE axes as needed
# plt.subplots_adjust(left=0.25, bottom=0.2, right=0.95, top=0.95)
#
#
# # Check Button widget
# labels = ['Daily Confirmed', 'Daily Discharged', 'Daily Recovery']
# activated = [True, True, True]
# axCheckButton = plt.axes([0.03, 0.4, 0.15, 0.15])
# chxbox = CheckButtons(axCheckButton, labels, activated)
#
#
# def showLine(label):
#     index = labels.index(label)
#     lines[index].set_visible(not lines[index].get_visible())
#     plt.draw()
#
#
# chxbox.on_clicked(showLine)
#
# ax.legend(loc='best')
# # plt.show()

