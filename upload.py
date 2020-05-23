import pyodbc

def initServer():
	print("Connecting to Server")
	#init server connection
	#driver = "{MySQL ODBC 8.0 Driver}"
	driver = "{ODBC Driver 13 for SQL Server}"
	server = "127.0.0.1"
	database = "tracker"
	username = "root"
	password = "Password!"
	#conn = pyodbc.connect("Driver="+driver+";SERVER="+server+";DATABASE="+database+";USER="+username+";PASSWORD="+password+";")
	conn = pyodbc.connect("DSN=dsn;UID=root;PWD=Password!")
	#conn = pyodbc.connect("driver="+driver+";server="+server+";database="+database+";user="+username+";password="+password+";")

	print("Success!")	
	return conn


def refreshClickDatabase():
	print("Loading Mouse Data...")
	global conn
	cursor = conn.cursor()

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

	clickLocData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickPlace.txt","w")
	clickTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\clickTime.txt", "w")

	clickLocData.write("")
	clickTimeData.write("")
	print("Done")

def refreshTypeDatabase():
	print("Loading Keyboard Data...")
	global conn
	cursor = conn.cursor()

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
	typeCharData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeChar.txt", "w")
	typeTimeData = open("C:\\Users\\aquin\\Documents\\Code\\C++\\TyperTracker\\TyperTracker\\typeTime.txt", "w")
	typeCharData.write("")
	typeTimeData.write("")
	print("Done")


conn = initServer()
refreshClickDatabase()
refreshTypeDatabase()
