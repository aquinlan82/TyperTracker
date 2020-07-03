import pyodbc
import os
import sys

""" Connect to Server """
def initServer(windows):
	print("Connecting to Server")
	if windows:
		driver = "{ODBC Driver 13 for SQL Server}"
	else:
		driver = "{MySQL ODBC 8.0 Driver}"
	server = "127.0.0.1"
	database = "tracker"
	username = "root"
	password = "Password!"
	if windows:
		conn = pyodbc.connect("DSN=dsn;UID=root;PWD=Password!")
	else:
		conn = pyodbc.connect("Driver="+driver+";SERVER="+server+";DATABASE="+database+";USER="+username+";PASSWORD="+password+";")

	print("Success!")	
	return conn

""" Determines if using windows or linux os """
def getWindows():
	interpretor = sys.executable
	if interpretor == "/usr/bin/python3":
		return False
	return True

""" Get directory for program """
def getBase(windows):
	base = os.getcwd()
	if windows:
		return base + "\\"
	return base + "/TyperTracker/"

""" Figure out valid range based on start and end dates """
def getWhereString(start, end):
	#For readability
	startDay = start[0]
	startMonth = start[1]
	startYear = start[2]
	endDay = end[0]
	endMonth = end[1]
	endYear = end[2]

	if startYear == endYear and startMonth == endMonth:
		day =  "day_ >= " + startDay + " and day_ <= " + endDay
		month = " and month_ >= " + startMonth + " and month_ <= " + endMonth
		year =  " and year_ >= " + startYear + " and year_ <= " + endYear
		query = day + month + year
		return query
	if startYear == endYear and startMonth != endMonth:
		month1 = "(month_ > " + startMonth + " and month_ < " + endMonth + ")" 
		month2 = "(month_ = " + startMonth + " and day_ >= " + startDay + ")"
		month3 = "(month_ = " + endMonth + " and day_ <= " + startDay + ")"
		year = "(year_ >= " + startYear + " and year_ <= " + endYear + ")"
		query = "(" + month1 + " or " + month2 + " or " + month3 + ") and " + year
		return query  
	if startYear != endYear:
		year1 = "year_ = " + startYear
		month1 = "(month_ >= " + startMonth + " or (month_ = " + startMonth + " and day_ >= " + startDay + "))"
		year2 = "year_ = " + endYear
		month2 = "(month_ <= " + endMonth + " or (month_ = " + endMonth + " and day_ <= " + endDay + "))"
		option3 = "year_ != " + startYear + " and year_ != " + endYear 
		query = "(" + year1 + " and " + month1 + ") or (" + year2 + " and " + month2 + ") or (" + option3 + ")"
		return query
	







