import sys
sys.path.append("../data-severity")
sys.path.append("../data-vaccination")
import tkinter as tk
from tkinter import *
import pygetwindow
import pyautogui
import os
import csv
from PIL import Image
import severity_dataset as sd
import recovery_dataset as rd
import vaccination_dataset as vd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# list that can be used by the dropdown button
yearList = ["2020", "2021"]
monthList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]


# input: month and year
# return: a figure consists of 4 graphs
def showGraph(month, year):
    # create a figure
    figure1 = plt.Figure(figsize=(19, 9), dpi=100, tight_layout=True)

    # first Graph
    ax1 = figure1.add_subplot(221)
    bar1 = FigureCanvasTkAgg(figure1, topFrame)
    bar1.get_tk_widget().grid(row=0, column=0)
    ds = sd.sortByDate(sd.severityRateDF, month, year)
    ds = ds[['DailyICU', 'DailyOxygen']]
    ds.plot(kind='barh', title="Total Hospitalisation", legend=True, fontsize=8, stacked=True, ax=ax1, color=['blue','orange'])
    ax1.set_title('Daily Severe Cases')
    ax1.set(ylabel="Date")
    ax1.set(xlabel="Cases")
    # ax1.yaxis.grid(True)
    # ax1.xaxis.grid(True)

    #Second Graph
    ax2 = figure1.add_subplot(222)
    bar2 = FigureCanvasTkAgg(figure1, topFrame)
    bar2.get_tk_widget().grid(row=0, column=0)
    dcs = sd.sortByDate(rd.mergeDataFrame, month, year)
    dcs.plot(title="Test", legend=True, fontsize=8, ax=ax2)
    ax2.set_title('Daily Confirmed, Discharged and Recover')
    ax2.set(ylabel="Cases")
    ax2.set(xlabel="Date")
    ax2.yaxis.grid(True)
    ax2.xaxis.grid(True)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
    
    # THIRD GRAPH
    ax3 = figure1.add_subplot(223)
    bar2 = FigureCanvasTkAgg(figure1, topFrame)
    bar2.get_tk_widget().grid(row=0,column=0) 
    vr = sd.sortByDate(vd.newdf, month, year)
    if month != 0:
        vr = vr[['FirstDose(%)', 'SecondDose(%)']]
    else:
        vr = sd.reCalculateRate(vr, 'population', ['people_vaccinated'], 'FirstDose(%)')
        vr = sd.reCalculateRate(vr, 'population', ['people_fully_vaccinated'], 'SecondDose(%)')
        vr = vr[['FirstDose(%)', 'SecondDose(%)']]
    vr.plot(title='Vaccination Rate(%)', legend=True, fontsize=8, ax=ax3)
    ax3.set(ylabel='Population(%)')
    ax3.set(xlabel='Date')
    ax3.legend(['1st Dose', '2nd Dose'])
    ax3.yaxis.grid(True)
    ax3.xaxis.grid(True)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)

# FOURTH GRAPH
    ax4 = figure1.add_subplot(224)
    bar3 = FigureCanvasTkAgg(figure1, topFrame)
    bar3.get_tk_widget().grid(row=0, column=0)
    rr = sd.sortByDate(vd.df2, month, year)
    if month != 0:
        ar = rr[['recovery_rate', 'two_dose']]
        br = rr[['SeverityRate(%)']]
    else:
        ar = sd.reCalculateRate(rr, 'cumulative_confirmed', ['cumulative_discharged'], 'recovery_rate')
        ar = sd.reCalculateRate(rr, 'population', ['people_fully_vaccinated'], 'SecondDose(%)')
        ar = rr[['recovery_rate', 'SecondDose(%)']]
        br = sd.reCalculateRate(rr, 'DailyCases', ['DailyICU', 'DailyOxygen'], 'SeverityRate(%)')['SeverityRate(%)']
    ax5 = ax4.twinx()
    br.plot(legend=True, fontsize=8, ax=ax4, color='red')
    ax4.set(ylabel='Rate(%)')
    ax4.legend(['Severity'], loc='upper left')
    ar.plot(title='Recovery vs Severity vs Vaccination', legend=True, fontsize=8, ax=ax5)
    ax4.legend(['Recovery', 'Vaccination'], loc='upper right')
    ax4.set(ylabel='Population(%)')
    ax4.set(xlabel='Date')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=90)
    ax4.yaxis.grid(True)
    ax4.xaxis.grid(True)

    g1 = Button(bottomFrame, text="Graph1", command=lambda: plotGraph1(ds))
    g1.grid(row=2, column=3)
    g2 = Button(bottomFrame, text="Graph2", command=lambda: plotGraph2(dcs))
    g2.grid(row=2, column=4)
    g3 = Button(bottomFrame, text="Graph3", command=lambda: plotGraph3(vr))
    g3.grid(row=2, column=5)
    g4 = Button(bottomFrame, text="Graph4", command=lambda: plotGraph4(br,ar))
    g4.grid(row=2, column=6)

    export = Button(bottomFrame, text="Export", command=lambda: writeToCsv(rr))
    export.grid(row=2, column=7)


def writeToCsv(df):
    df.to_csv("export.csv", index=True)
    fln = tk.filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"),
                                                                                               ("All Files", "*.*")))
    with open(fln, mode='w', encoding="utf-8"):
        df.to_csv("export.csv", index=True)
    tk.messagebox.showinfo("Data Exported", "The data has been written to " + os.path.basename(fln) + " successfully.")


def plotGraph1(ds):
    ds = ds[['DailyICU', 'DailyOxygen']]
    ax1 = ds.plot(kind='barh', title="Total Hospitalisation", legend=True, fontsize=8, stacked=True,
            color=['blue', 'orange'])
    ax1.set_title('Daily Severe Cases')
    ax1.set(ylabel="Date")
    ax1.set(xlabel="Cases")
    plt.show()


def plotGraph2(dcs):
    ax2 = dcs.plot(title="Test", legend=True, fontsize=8)
    ax2.set_title('Daily Confirmed, Discharged and Recover')
    ax2.set(ylabel="Cases")
    ax2.set(xlabel="Date")
    ax2.yaxis.grid(True)
    ax2.xaxis.grid(True)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=90)
    plt.show()


def plotGraph3(vr):
    ax3= vr.plot(title='Vaccination Rate(%)', legend=True, fontsize=8)
    ax3.set(ylabel='Population(%)')
    ax3.set(xlabel='Date')
    ax3.legend(['1st Dose', '2nd Dose'])
    ax3.yaxis.grid(True)
    ax3.xaxis.grid(True)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
    plt.show()


def plotGraph4(br,ar):
    ax4 = br.plot(legend=True, fontsize=8, color='red')
    ax5 = ax4.twinx()
    ax4.set(ylabel='Rate(%)')
    ax4.legend(['Severity'], loc='upper left')
    ar.plot(title='Recovery vs Severity vs Vaccination', legend=True, fontsize=8,ax=ax5)
    ax4.legend(['Recovery', 'Vaccination'], loc='upper right')
    ax4.set(ylabel='Population(%)')
    ax4.set(xlabel='Date')
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=90)
    ax4.yaxis.grid(True)
    ax4.xaxis.grid(True)
    plt.show()

# clear all the widget in the top frame
def clearGraph():
    for widget in topFrame.winfo_children():
        widget.destroy()

        
# unhide the radioButton        
def sMonth(month, e):
    month.set("1")
    e.grid(row=0, column=3)

    
# set the value to 0 and hide it
def sYear(month, e):
    month.set("0")
    e.grid_forget()


# save a screenshot according to window size
def save():
    window = pygetwindow.getWindowsWithTitle('Covid19 Analyser')[0]
    x1 = window.left
    y1 = window.top
    h = window.height
    w = window.width

    x2 = x1 + w
    y2 = y1 + h
    pyautogui.screenshot("result.png")

    im = Image.open('result.png')
    im = im.crop((x1, y1, x2, y2))
    im.save('result.png')
    im.show('result.png')


root = tk.Tk()
root.title("Covid19 Analyser")
root.geometry("1800x900")

# initialise 2 frame
topFrame = Frame(root)
topFrame.grid(row=0, column=0)
bottomFrame = Frame(root)
bottomFrame.grid(row=1, column=0)

# initialise type of value and set default value
clicked, clicked2 = IntVar(), IntVar()
clicked.set("2021")
clicked2.set("10")

# initialise 2 dropdown menus
dropYear = OptionMenu(bottomFrame, clicked, *yearList)
dropYear.grid(row=0, column=2)
dropMonth = OptionMenu(bottomFrame, clicked2, *monthList)
dropMonth.grid(row=0, column=3)

# initialise 2 buttons
submitB = Button(bottomFrame, text="Submit", command=lambda: showGraph(clicked2.get(), clicked.get()))
submitB.grid(row=2, column=0)
clearB = Button(bottomFrame, text="Clear", command=clearGraph)
clearB.grid(row=2, column=1)
saveB = Button(bottomFrame, text="Save", command=save)
saveB.grid(row=2, column=2)


# initialise 2 radio buttons
mode= IntVar()
mode.set(1)
sortbyMonthRB = Radiobutton(bottomFrame, text="ByMonth", variable=mode, value=1, command=lambda: sMonth(clicked2, dropMonth)).grid(row=0, column=0)
sortbyYearRB = Radiobutton(bottomFrame, text="ByYear", variable=mode, value=2, command=lambda: sYear(clicked2, dropMonth)).grid(row=0, column=1)

vd.df2.to_csv("clean_dataset.csv", index=True)

root.mainloop()
