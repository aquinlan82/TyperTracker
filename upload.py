import pyodbc
import os
import sys
import helper



""" Add txt file values to SQL """
def refreshClickDatabase():
	print("Loading Mouse Data...")
	entries = getArray("clickPlace.txt", "clickTime.txt", True)
	enterEntries(entries)
	eraseFiles("clickPlace.txt", "clickTime.txt")
	print("Done")


""" Add txt file values to SQL """
def refreshTypeDatabase():
	print("Loading Keyboard Data...")
	entries = getArray("typeChar.txt", "typeTime.txt", False)
	enterEntries(entries)
	eraseFiles("typeChar.txt", "typeTime.txt")
	print("Done")

"""Creates array of data in txt files """
def getArray(place, time, coords):
	entries = []
	clickLocData = open(base + place)
	clickTimeData = open(base + time)
	while True:
		try:
			x = clickLocData.readline().strip()
			y = ""
			if coords:
				y = clickLocData.readline().strip()
			time = clickTimeData.readline().strip()
			year = str(int(str(time)[0:2])+8)
			month = str(int(str(time)[2:4])+1)
			day = str(time)[4:6]
			hour = "3"
			minute = "2"
			if coords:
				temp = [x,y,day,month,year,hour,minute]
			else:
				temp = [x,day,month,year,hour,minute]
			entries.append(temp)
		except:
			break
	print("Array constructed... " + str(len(entries)) + " entries")
	return entries

"""Change character if problem with escape characters """
def scanForProblems(char):
	if char == "\\":
		return "\\\\"
	else:
		return char

"""Add array entries to SQL """
def enterEntries(entries):
	global conn
	cursor = conn.cursor()
	i = 0
	for entry in entries:
		entry = [str(i) for i in entry]
		try:
			string = ""
			if len(entry) == 7:
				string = "insert into tracker.Clicks values ("+entry[0]+","+entry[1]+","+entry[2]+","+entry[3]+","+entry[4]+","+entry[5]+","+entry[6]+")"
			else:
				entry[0] = scanForProblems(entry[0])
				string = "insert into tracker.Chars values (\""+str(entry[0])+"\","+entry[1]+","+entry[2]+","+entry[3]+","+entry[4]+","+entry[5]+")"

			cursor.execute(string)
			conn.commit()
			if i % 20 == 0:
				print("Entering entry " + str(i) + " of " + str(len(entries)))
			i = i + 1
		except:
			print("error with " + string)
	print("Done entering... Hold on a moment")

"""	Deletes data in the file """
def eraseFiles(first, second):
	clickLocData = open(base + first,"w")
	clickTimeData = open(base + second, "w")
	clickLocData.write("")
	clickTimeData.write("")



""" Main Method """
windows = helper.getWindows()
global base
base = helper.getBase(windows)

conn = helper.initServer(windows)
refreshClickDatabase()
refreshTypeDatabase()
