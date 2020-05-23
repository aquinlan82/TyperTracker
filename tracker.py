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

def initServer():
	print("Connecting to Server")
	#init server connection
	#driver = "{MySQL ODBC 8.0 Driver}"
	driver = "{ODBC Driver 13 for SQL Server}"
	server = "127.0.0.1"
	database = "tracker"
	username = "root"
	password = "Password!"
	#conn = pyodbc.connect("driver="+driver+";server="+server+";database="+database+";user="+username+";password="+password+";")
	conn = pyodbc.connect("DSN=dsn;UID=root;PWD=Password!")

	print("Success!")	
	return conn


def refreshClickDatabase():
	print("Loading Mouse Data...")
	global conn
	cursor = conn.cursor()

	#clickLocData = open("TyperTracker/clickPlace.txt")
	#clickTimeData = open("TyperTracker/clickTime.txt")
	clickLocData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickPlace.txt")
	clickTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickTime.txt")
	
	while True:
		x = clickLocData.readline().strip()
		if x == "":
			break
		else:
			y = clickLocData.readline().strip()
			time = clickTimeData.readline().strip()
			year = str(int(str(time)[0:2])+8)
			month = str(int(str(time)[2:4])+1)
			day = str(time)[4:6]
			hour = "3"
			minute = "2"
			
			string = "insert into tracker.Clicks values ("+x+","+y+","+day+","+month+","+year+","+hour+","+minute+")"
			cursor.execute(string)
			conn.commit()
	#clickLocData = open("TyperTracker/clickPlace.txt", "w")
	#clickTimeData = open("TyperTracker/clickTime.txt", "w")
	clickLocData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickPlace.txt","w")
	clickTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickTime.txt", "w")

	clickLocData.write("")
	clickTimeData.write("")
	print("Done")

def refreshTypeDatabase():
	print("Loading Keyboard Data...")
	global conn
	cursor = conn.cursor()

	#typeCharData = open("TyperTracker/typeChar.txt")
	#typeTimeData = open("TyperTracker/typeTime.txt")
	typeCharData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeChar.txt")
	typeTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeTime.txt")
	
	while True:
		c = typeCharData.readline().strip()
		if c == "":
			break
		else:
			time = typeTimeData.readline().strip()
			year = str(int(str(time)[0:2])+8)
			month = str(int(str(time)[2:4])+1)
			day = str(time)[4:6]
			hour = "3"
			minute = "2"
			
			string = "insert into tracker.Chars values (\""+c+"\","+day+","+month+","+year+","+hour+","+minute+")"
			cursor.execute(string)
			conn.commit()
	#typeCharData = open("TyperTracker/typeChar.txt", "w")
	#typeTimeData = open("TyperTracker/typeTime.txt", "w")
	typeCharData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeChar.txt", "w")
	typeTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeTime.txt", "w")
	
	typeCharData.write("")
	typeTimeData.write("")
	print("Done")


def getClickLocCursor(time1, time2):
	print("Accessing Mouse Data")
	#time = [day, month, year, hour,minute]
	global conn
	cursor = conn.cursor()
	string = "select X,Y from tracker.Clicks where day_ >= "+time1[0]+" and day_ <= "+time2[0]+" and month_ >= "+time1[1]+" and month_ <= "+time2[1]+" and year_ >= "+time1[2]+" and year_ <= "+time2[2]
	cursor.execute(string)
	return cursor

def getTypeCharCursor(time1, time2):
	print("Accessing Keyboard Data")
	#time = [day, month, year, hour,minute]
	global conn
	cursor = conn.cursor()
	string = "select char_ from tracker.Chars where day_ >= "+time1[0]+" and day_ <= "+time2[0]+" and month_ >= "+time1[1]+" and month_ <= "+time2[1]+" and year_ >= "+time1[2]+" and year_ <= "+time2[2]
	cursor.execute(string)
	return cursor

def getTimeCursor(time1, time2, click):
	print("Accessing Time Data")
	#time = [day, month, year, hour,minute]
	if click:
		db = "Clicks"
	else:
		db = "Chars"
	global conn
	cursor = conn.cursor()
	string = "select day_, month_, year_, hour_, minute_ from tracker."+db+" where day_ >= "+time1[0]+" and day_ <= "+time2[0]+" and month_ >= "+time1[1]+" and month_ <= "+time2[1]+" and year_ >= "+time1[2]+" and year_ <= "+time2[2]
	cursor.execute(string)
	return cursor

def getTypeCharAxes(time1, time2):
	print("Sorting Keyboard Data")
	#get relevant points based on time
	points = getTypeCharCursor(time1, time2)
	dictFreq = {}
	for point in points:
		if point[0] in dictFreq:
			dictFreq[point[0]] = dictFreq[point[0]] + 1
		else:
			dictFreq[point[0]] = 1
	return dictFreq

def getClickLocAxes(time1, time2):
	print("Sorting Mouse Data")
	#get relevant points based on time
	points = getClickLocCursor(time1, time2)

	#organize x, y, and freq into dictionary
	dictFreq = {}
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


def getTimeAxes(time1, time2, scale, click):
	print("Sorting Time Data")
	#get relevant points based on time
	#point = [day, month, year, hour, minute]
	points = getTimeCursor(time1, time2, click)
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

def dateStringToArray(string):
	#converts string in m/d/y to array in [d,m,y]
	temp = string.split("/")
	if len(temp[2]) > 2:
		temp[2] = temp[2][2:4]
	out = [temp[1], temp[0], temp[2]]
	return out

def updateMouseHeat():	
	global MHstartIn
	global MHendIn
	global mouseHeatPlot
	global mouseHeatCanvas
	start = dateStringToArray(MHstartIn.get())
	end = dateStringToArray(MHendIn.get())
	x,y,freq = getClickLocAxes(start,end)
	f = Figure()
	mouseHeatPlot = f.add_subplot(111)
	mouseHeatPlot.scatter(x,y, c=freq)
	mouseHeatCanvas = FigureCanvasTkAgg(f, clickHeatTab)
	crs = mplcursors.cursor(mouseHeatPlot,hover=True)
	crs.connect("add", lambda sel: sel.annotation.set_text(
		'Point: {},{} \nClicked: {} times'.format(sel.target[0], sel.target[1], freq[sel.target.index])))
	#mouseHeatCanvas.show()
	mouseHeatCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)

def updateTypeHeat():
	global typeHeatCanvas
	dictFreq = getTypeCharAxes(start, end)
	typeHeatCanvas = Canvas(typeHeatTab, width=750, height=250, bg="#788279")
	drawKeyboard(typeHeatCanvas, dictFreq)
	typeHeatCanvas.grid(row=3, column=1,columnspan=3, pady=50, padx=25)

def updateMouseTime():
	global MTstartIn
	global MTendIn
	global mouseTimePlot
	global mouseTimeCanvas
	start = dateStringToArray(MTstartIn.get())
	end = dateStringToArray(MTendIn.get())
	times,freqs = getTimeAxes(start,end,scale,True)
	f = Figure()
	mouseTimePlot = f.add_subplot(111)
	mouseTimePlot.plot(times, freqs, marker="o")
	mouseTimeCanvas = FigureCanvasTkAgg(f, clickGraphTab)
	crs = mplcursors.cursor(mouseTimePlot,hover=True)
	crs.connect("add", lambda sel: sel.annotation.set_text(
		'Clicks: {}'.format(sel.target[1])))
	#mouseTimeCanvas.show()
	mouseTimeCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)

def updateTypeTime():
	global TTstartIn
	global TTendIn
	global typeTimePlot
	global typeTimeCanvas
	start = dateStringToArray(TTstartIn.get())
	end = dateStringToArray(TTendIn.get())
	times,freqs = getTimeAxes(start,end,scale,False)
	f = Figure()
	typeTimePlot = f.add_subplot(111)
	typeTimePlot.plot(times, freqs, marker="o")
	typeTimeCanvas = FigureCanvasTkAgg(f, typeGraphTab)
	crs = mplcursors.cursor(typeTimePlot,hover=True)
	crs.connect("add", lambda sel: sel.annotation.set_text(
		'Characters: {}'.format(sel.target[1])))
	#typeTimeCanvas.show()
	typeTimeCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)




#/////////////////////////
conn = initServer()
now =datetime.now()
now = now.strftime("%m/%d/%Y")

#ans = input("Load data to SQL? ")
#if ans == "y":
#	refreshClickDatabase()
#	refreshTypeDatabase()

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

#Mouse Heat Tab
Label(clickHeatTab, text="From").grid(row=1,column=1)
MHstartIn = Entry(clickHeatTab)
MHstartIn.insert(0,"5/17/2020")
MHstartIn.grid(row=2, column=1)
Label(clickHeatTab, text="To").grid(row=1, column=2)
MHendIn = Entry(clickHeatTab)
MHendIn.insert(0,now)
MHendIn.grid(row=2, column=2)
start = dateStringToArray(MHstartIn.get())
end = dateStringToArray(MHendIn.get())
Button(clickHeatTab, text="Go", command=updateMouseHeat).grid(row=1,column=3,rowspan=2)

x,y,freq = getClickLocAxes(start,end)
f = Figure()
mouseHeatPlot = f.add_subplot(111)
mouseHeatPlot.scatter(x,y, c=freq)
mouseHeatCanvas = FigureCanvasTkAgg(f, clickHeatTab)
crs = mplcursors.cursor(mouseHeatPlot,hover=True)
crs.connect("add", lambda sel: sel.annotation.set_text(
    'Point: {},{} \nClicked: {} times'.format(sel.target[0], sel.target[1], freq[sel.target.index])))
#mouseHeatCanvas.show()
mouseHeatCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)

#Key Heat Tab
Label(typeHeatTab, text="From").grid(row=1,column=1)
THstartIn = Entry(typeHeatTab)
THstartIn.insert(0,"5/17/2020")
THstartIn.grid(row=2, column=1)
Label(typeHeatTab, text="To").grid(row=1, column=2)
THendIn = Entry(typeHeatTab)
THendIn.insert(0,now)
THendIn.grid(row=2, column=2)
start = dateStringToArray(THstartIn.get())
end = dateStringToArray(THendIn.get())
Button(typeHeatTab, text="Go", command=updateTypeHeat).grid(row=1,column=3,rowspan=2)

dictFreq = getTypeCharAxes(start, end)
typeHeatCanvas = Canvas(typeHeatTab, width=750, height=250, bg="#788279")
drawKeyboard(typeHeatCanvas, dictFreq)
typeHeatCanvas.grid(row=3, column=1,columnspan=3, pady=50, padx=25)

#Mouse Stats Tab
scale = "day"

Label(clickGraphTab, text="From").grid(row=1,column=1)
MTstartIn = Entry(clickGraphTab)
MTstartIn.insert(0,"5/17/2020")
MTstartIn.grid(row=2, column=1)
Label(clickGraphTab, text="To").grid(row=1, column=2)
MTendIn = Entry(clickGraphTab)
MTendIn.insert(0,now)
MTendIn.grid(row=2, column=2)
start = dateStringToArray(MTstartIn.get())
end = dateStringToArray(MTendIn.get())
Button(clickGraphTab, text="Go", command=updateMouseTime).grid(row=1,column=3,rowspan=2)

times,freqs = getTimeAxes(start,end,scale,True)
f = Figure()
mouseTimePlot = f.add_subplot(111)
mouseTimePlot.plot(times, freqs, marker="o")
mouseTimeCanvas = FigureCanvasTkAgg(f, clickGraphTab)
crs = mplcursors.cursor(mouseTimePlot,hover=True)
crs.connect("add", lambda sel: sel.annotation.set_text(
    'Clicks: {}'.format(sel.target[1])))
#mouseTimeCanvas.show()
mouseTimeCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)

#Key Stats Tab
scale = "day"

Label(typeGraphTab, text="From").grid(row=1,column=1)
TTstartIn = Entry(typeGraphTab)
TTstartIn.insert(0,"5/17/2020")
TTstartIn.grid(row=2, column=1)
Label(typeGraphTab, text="To").grid(row=1, column=2)
TTendIn = Entry(typeGraphTab)
TTendIn.insert(0,now)
TTendIn.grid(row=2, column=2)
start = dateStringToArray(TTstartIn.get())
end = dateStringToArray(TTendIn.get())
Button(typeGraphTab, text="Go", command=updateTypeTime).grid(row=1,column=3,rowspan=2)

times,freqs = getTimeAxes(start,end,scale,False)
f = Figure()
typeTimePlot = f.add_subplot(111)
typeTimePlot.plot(times, freqs, marker="o")
typeTimeCanvas = FigureCanvasTkAgg(f, typeGraphTab)
crs = mplcursors.cursor(typeTimePlot,hover=True)
crs.connect("add", lambda sel: sel.annotation.set_text(
    'Characters: {}'.format(sel.target[1])))
#typeTimeCanvas.show()
typeTimeCanvas.get_tk_widget().grid(row=3, column=1,columnspan=3, pady=30, padx=30)

#Loop
root.mainloop()
