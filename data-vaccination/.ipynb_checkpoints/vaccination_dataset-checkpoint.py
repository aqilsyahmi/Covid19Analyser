import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

mainDir = Path(__file__).parent.parent
path = Path(__file__).parent
sys.path.append('../data-severity/')
import severity_dataset as sd


df = pd.read_csv(str(mainDir)+"\data-severity\owid-covid-data.csv")[lambda x: x['location'] == 'Singapore']
df2 = pd.read_csv(str(path)+"\covid_19_sg.csv")

df2.columns = df2.columns.str.lower()

df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")
df2['date'] = pd.to_datetime(df2['date'], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")

df = df.set_index("date")
df2 = df2.set_index("date")
df.index = pd.to_datetime(df.index)
df.index = df.index.date
df2.index = pd.to_datetime(df2.index)
df2.index = df2.index.date

df = df[['people_vaccinated', 'population', 'people_fully_vaccinated']]
df2 = df2[['cumulative_discharged', 'cumulative_confirmed']]

newdf = df.interpolate()
newdf["FirstDose(%)"] = (newdf["people_vaccinated"] / newdf["population"])*100
newdf["SecondDose(%)"] = (newdf["people_fully_vaccinated"] / newdf["population"])*100

df2["recovery_rate"]= (df2["cumulative_discharged"]/df2["cumulative_confirmed"])*100
df2 = df2.join(newdf[["two_dose", "population", "people_fully_vaccinated"]])
df2 = df2.join(sd.severityRateDF[["SeverityRate(%)", 'DailyCases', 'DailyICU', 'DailyOxygen']])



#
# change the format of date to datetime
# to filter the date range, values of date can be assigned manually below
#
def filterByDate(DataFrame, StartDate, EndDate, Frequency):
    DataFrame['date'] = pd.to_datetime(DataFrame['date'])
    filtered_df = DataFrame.ffill().bfill().resample(Frequency, on='date').mean()
    filtered_df.reset_index(inplace=True)
    mask = (filtered_df['date'] >= StartDate) & (filtered_df['date'] <= EndDate)
    filtered_df2 = filtered_df.loc[mask]
    return filtered_df2

# # -------------------------------------------------------------------------------------------------
# # BELOW ONE IS FOR SELF TESTING PURPOSE
# #
# #   interpolate to fill up NAN with mean/average
# #
# vaccination_filter_df = df.interpolate()
#
# #
# #   Sort the dataframe according to the selected month
# #   Call function from symptoms_dataset to sort the date
# #
# filtered_df = sd.sortByDate(df,10,2021)
# filtered_df2 = sd.sortByDate(df2,10,2021)
# severityRateDF = sd.calculateSeverityRate(sd.mergeTable)
# filtered_severityRateDF = sd.sortByDate(severityRateDF,10,2021)
#
#
# #
# #   To plot graph with 2 rows
# #
# fig, axs = plt.subplots(2)
#
# # --------------------------------------- FIRST GRAPH --------------------------------------------
# # using vaccination_filter_df to show all dates for data-vaccination
# line1 = axs[0].plot((vaccination_filter_df["people_vaccinated"] / df["population"]) * 100, label='Completed one dose')
# line2 = axs[0].plot((vaccination_filter_df["people_fully_vaccinated"] / df["population"]) * 100, label='Completed data-vaccination')
# axs[0].legend(loc="upper left")
# axs[0].set(ylabel="Population(%)")
# axs[0].yaxis.grid(True)
# axs[0].xaxis.grid(True)
# # Format date according to your choice, %b means Jan, Feb etc. %b-%y will show Jan-2021
# # myFmt = mdates.DateFormatter('%b-%y')
# # axs[0].xaxis.set_major_formatter(myFmt)
# #axs[0].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
# #
# # Convert the values of col into percentage
# # axs[0].set_yticklabels(['{:,.0%}'.format(x) for x in axs[0].get_yticks()])
# #
# # Set the axis label
# plt.setp(axs[0].xaxis.get_majorticklabels(), rotation=90)
#
# # ------------------------------------------------------------------------------------------------
#
# # --------------------------------------SECOND GRAPH ---------------------------------------------
# # to create another y axis to indicate the data-vaccination rate
# axs2 = axs[1].twinx()
# line3 = axs2.plot((filtered_df["people_fully_vaccinated"]/filtered_df["population"] * 100), color='green', label='Fully vaccinated')
# line4 = axs[1].plot(filtered_severityRateDF["SeverityRate(%)"], color='red', label='Severity Rate per daily cases')
# #line5 = axs[1].plot(((filtered_df2["cumulative_confirmed"]-filtered_df2["cumulative_discharged"])/filtered_df2["cumulative_confirmed"]), color='blue', label='Hospitalization Rate per daily cases')
# line5 = axs[1].plot(((filtered_df2["cumulative_discharged"])/filtered_df2["cumulative_confirmed"]), color='blue', label='Recovery Rate per daily cases')
#
# axs2.set(ylabel="Population (%)")
# axs[1].set(ylabel="Severity/Recovery Rate(%)")
# plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=90)
#
# axs[1].yaxis.grid(True)
# axs[1].xaxis.grid(True)
#
# # Complile the labels for the second graph and put it into a legend
# lns =line3 + line4 + line5
# labels = [l.get_label() for l in lns]
# plt.legend(lns, labels, loc='upper left')
#
# # plt.tight_layout()
# ## plt.show()
#
# # Format date according to your choice, %b means Jan, Feb etc. %b-%y will show Jan-2021
# # myFmt = mdates.DateFormatter('%d-%b-%y')
# # axs[1].xaxis.set_major_formatter(myFmt)
# # defines the label format
# # xticks = ticker.MaxNLocator(len(filtered_df2)//6)
#
# # axs[1].xaxis.set_major_locator(xticks)
#
# # axs[1].set(xticks=filtered_df2['date'].values)
# #axs[1].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))

# -------------------------------------------------------------------------------------------------

