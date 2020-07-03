import pyodbc
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import sys
from pandas import DataFrame
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
from keyboard import drawKeyboard
import mplcursors
import helper

""" Check that start is before end and dates make sense """
def timesAreValid(start, end):
	start = [int(i) for i in start]
	end = [int(i) for i in end]

	if len(start) != 3 or len(end) != 3:
		return False
	if start[1] > 12 or start[1] < 1 or end[1] > 12 or end[1] < 1:
		return False
	if start[0] < 1 or end[0] < 1:
		return False
	if start[2] > end[2]:
		return False
	if start[2] == end[2] and start[1] > end[1]:
		return False
	if start[2] == end[2] and start[1] == end[1] and start[0] > end[0]:
		return False
	return True

""" Creates string to send to SQL """
def constructQuery(start, end, select, db):
	selectString = "select " + select
	fromString = " from tracker." + db
	whereString = " where " + helper.getWhereString(start, end)
	query = selectString + fromString + whereString
	return query

""" Gets result of SQL query """
def getCursor(time1, time2, select, db):
	if timesAreValid(time1, time2):
		global conn
		cursor = conn.cursor()
		string = constructQuery(time1, time2, select, db)
		cursor.execute(string)
		return cursor
	
""" Organize keypress data into dictionary based on frequency pressed """
def getTypeCharAxes(time1, time2):
	points = getCursor(time1, time2, "char_", "Chars")
	dictFreq = {}
	for point in points:
		if point[0] in dictFreq:
			dictFreq[point[0]] = dictFreq[point[0]] + 1
		else:
			dictFreq[point[0]] = 1
	return dictFreq

""" Organize click coordinates into lists """
def getClickLocAxes(time1, time2):
	points = getCursor(time1, time2, "X,Y", "Clicks")
	dictFreq = {}
	# organize coordinates into dictionary based on frequency
	for point in points:
		x = point[0]
		y = point[1]
		if x in dictFreq:
			if y in dictFreq[x]:
				dictFreq[x][y] = dictFreq[x][y] + 1
			else:
				dictFreq[x].update({y : 1})
		else:
			dictFreq[x] = {y : 1}

	#turn dictionary into graph friendly lists
	x = []
	y = []
	freq = []
	for x_val in dictFreq.keys():
		y_vals = dictFreq[x_val]
		for y_val in y_vals:
			x.append(x_val)
			y.append(y_val)
			freq.append(dictFreq[x_val][y_val])
	return x,y, freq

""" Organize points into lists by frequency """
def getTimeAxes(time1, time2, scale, db):
	points = getCursor(time1, time2, " day_, month_, year_, hour_, minute_ ", db)

	dictFreq = {}
	for point in points:
		year = point[2]
		month = point[1]
		day = point[0]
		if year in dictFreq:
			if month in dictFreq[year]:
				if day in dictFreq[year][month]:
					dictFreq[year][month][day] = dictFreq[year][month][day] + 1
				else:
					dictFreq[year][month].update({day : 1})
			else:
				dictFreq[year].update({month : {day:1}})
		else:
			dictFreq[year] = {month:{day : 1}}

	#turn dictionary into graph friendly lists
	times = []
	freqs = []
	count = 0
	for year in dictFreq.keys():
		months = dictFreq[year]
		for month in months:
			days = dictFreq[year][month]
			for day in days:
				if scale == "day":
					label = str(month) + "/" + str(day) + "/" + str(year)
					times.append(label)
					freqs.append(dictFreq[year][month][day])
				else:
					count = count + 1
			if scale == "month":
				label = str(month) + "/" + str(year)
				times.append(label)
				freqs.append(count)
				count = 0
		if scale == "year":	
			label = "20" + str(year)
			times.append(label)
			freqs.append(count)
			count = 0
				
	return times, freqs

""" Returns endpoint dates in entry boxes """
def getDates(index):
	global startEntries
	global endEntries
	start = dateStringToArray(startEntries[index].get())
	end = dateStringToArray(endEntries[index].get())
	return start, end


""" Converts string in m/d/y to array in [d,m,y] """
def dateStringToArray(string):
	temp = string.split("/")
	if len(temp[2]) > 2:
		temp[2] = temp[2][2:4]
	out = [temp[1], temp[0], temp[2]]
	return out

""" Called when Go button is pressed on click click heat map tab """
def updateMouseHeat():	
	start, end = getDates(0)
	x,y,freq = getClickLocAxes(start,end)
	drawPlot(x,y,freq, clickHeatTab)

""" Called when Go button is pressed on keyboard tab """
def updateTypeHeat():
	start, end = getDates(1)
	dictFreq = getTypeCharAxes(start, end)
	canvas = Canvas(typeHeatTab, width=750, height=250, bg="#788279")
	drawKeyboard(canvas, dictFreq)
	canvas.grid(row=3, column=1,columnspan=3, pady=50, padx=25)

""" Called when Go button is pressed on click frequency tab """
def updateMouseTime():
	start, end = getDates(2)
	times,freqs = getTimeAxes(start,end,scale,"Clicks")
	drawPlot(times, None, freqs, clickGraphTab)

""" Called when Go button is pressed on type frequency tab """
def updateTypeTime():
	start, end = getDates(3)
	times,freqs = getTimeAxes(start,end,scale,"Chars")
	drawPlot(times, None, freqs, typeGraphTab)

""" Creates text input boxes for time range and sets default values """
def createDateEntries(tab, updateMethod):
	global startEntries
	global endEntries
	Label(tab, text="From").grid(row=1,column=1)
	startEntryBox = Entry(tab)
	startEntryBox.insert(0,"05/17/2020")
	startEntryBox.grid(row=2, column=1)
	Label(tab, text="To").grid(row=1, column=2)
	endEntryBox = Entry(tab)
	endEntryBox.insert(0,now)
	endEntryBox.grid(row=2, column=2)
	start = dateStringToArray(startEntryBox.get())
	end = dateStringToArray(endEntryBox.get())
	Button(tab, text="Go", command=updateMethod).grid(row=1,column=3,rowspan=2)
	startEntries.append(startEntryBox)
	endEntries.append(endEntryBox)
	return start, end

""" Plots points """
def drawPlot(x, y, freq, tab):
	f = Figure()
	plot = f.add_subplot(111)
	if y != None:
		plot.scatter(x,y, c=freq)
	else:
		plot.plot(x, freq, marker="o")
	plot.set_xticklabels(plot.get_xticklabels(), rotation="vertical")
	canvas = FigureCanvasTkAgg(f, tab)
	crs = mplcursors.cursor(plot,hover=True)
	if y != None:
		crs.connect("add", lambda sel: sel.annotation.set_text(
			'Point: {},{} \nClicked: {} times'.format(sel.target[0], sel.target[1], freq[sel.target.index])))
	else:
		crs.connect("add", lambda sel: sel.annotation.set_text(
			'Characters: {}'.format(sel.target[1])))
	canvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)


""" Main Method """
conn = helper.initServer(helper.getWindows())
now =datetime.now()
now = now.strftime("%m/%d/%Y")
print("Loading Data")

#window settings
winLen = 800
winHei = 570
root = Tk()
root.title("Tracker")
root.geometry(str(winLen)+"x"+str(winHei))

#tabs
tabPane = ttk.Notebook(root)
clickHeatTab = ttk.Frame(tabPane)
typeHeatTab = ttk.Frame(tabPane)
clickGraphTab = ttk.Frame(tabPane)
typeGraphTab = ttk.Frame(tabPane)

tabPane.add(clickHeatTab, text = "Mouse Heat Map")
tabPane.add(typeHeatTab, text = "Keyboard Heat Map")
tabPane.add(clickGraphTab, text = "Mouse Stats")
tabPane.add(typeGraphTab, text = "Keyboard Stats")

tabPane.pack(expand=1, fill="both")
global startEntries
global endEntries
startEntries = []
endEntries = []

#Mouse Heat Tab
start, end = createDateEntries(clickHeatTab, updateMouseHeat)
x,y,freq = getClickLocAxes(start,end)
drawPlot(x,y,freq, clickHeatTab)

#Key Heat Tab
start, end = createDateEntries(typeHeatTab, updateTypeHeat)
dictFreq = getTypeCharAxes(start, end)
canvas = Canvas(typeHeatTab, width=750, height=250, bg="#788279")
drawKeyboard(canvas, dictFreq)
canvas.grid(row=3, column=1,columnspan=3, pady=50, padx=25)

#Mouse Stats Tab
scale = "day"
start, end = createDateEntries(clickGraphTab, updateMouseTime)
times,freqs = getTimeAxes(start,end,scale,"Clicks")
drawPlot(times, None, freqs, clickGraphTab)

#Key Stats Tab
scale = "day"
start, end = createDateEntries(typeGraphTab, updateTypeTime)
times,freqs = getTimeAxes(start,end,scale,"Chars")
drawPlot(times, None, freqs, typeGraphTab)

#Loop
root.mainloop()
