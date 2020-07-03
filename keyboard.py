boxes = []
values = {}

""" File contains large helper methods for creating keyboard interface since it is bulky
and doesn't contain a lot of patterns to make better """



""" Create label displaying count for key that mouse is over """
def hover(event, canvas, labelId, rectId):
	width = 70
	height = 20
	count = getBoxCount(event.x, event.y)
	if count == "NA":
		canvas.coords(labelId, -100, event.y)
		canvas.coords(rectId, -100, event.y-height/2, -100+width, event.y+height/2)
	else:
		canvas.itemconfig(labelId, text=str(count) + " times")
		canvas.coords(labelId, event.x + 30, event.y)
		canvas.coords(rectId, event.x, event.y-height/2, event.x+width, event.y+height/2)

""" Each box represents one key with two location coordinates and a color """
def storeBox(x,y,x2,y2,color):
	global boxes 
	boxes.append([x,y,x2,y2,color])

""" Based on location, get the color of the key at that place """
def getBoxCount(x,y):
	global values
	for box in boxes:
		if x > box[0] and x < box[2] and y > box[1] and y < box[3]:
			#use color to get count
			return values[box[4]]
	return "NA"

""" Get r value based on percentile. Colors bounce between 69 and 196, each color is 20 percents long """
def getRed(per):
	step = (196 - 69)/ 20
	if per < 20:
		return 196 - step * per
	if per >=20 and per < 60:
		return 69
	if per >=60 and per < 80:
		return 69 + step * (per - 60)
	return 196

""" Get g value based on percentile. Colors bounce between 69 and 196, each color is 20 percents long """
def getGreen(per):
	step = (196 - 69)/ 20
	if per < 20:
		return 69
	if per >= 20 and per < 40:
		return 69 + (per - 20) * step
	if per >= 40 and per < 80:
		return 196
	return 196 - (per - 80) * step


""" Get b value based on percentile. Colors bounce between 69 and 196, each color is 20 percents long """
def getBlue(per):
	step = (196 - 69)/ 20
	if per < 40:
		return 196
	if per >= 40 and per < 60:
		return 196 - (per - 40) * step
	return 69

""" Translate rgb into hex code """
def getHex(r,g,b):
	hr = hex(int(r))[2:]
	hg = hex(int(g))[2:]
	hb = hex(int(b))[2:]
	return "#" + hr+hg+hb

""" Based on relative frequency, assign each key a color """
def setColors(dictFreq, validChars):
	#sort dictionary and get percentiles list
	dictFreq = {k: v for k, v in sorted(dictFreq.items(), key=lambda item: item[1])}
	percentiles = list(dictFreq.values())
	vals = percentiles.copy()
	for i in range(len(percentiles)):
		if i != 0 and vals[i-1] == vals[i]:
			percentiles[i] = percentiles[i-1]
		else:
			percentiles[i] = (i+1) / len(percentiles) * 100

	#use percentiles to get color
	colors = []
	for per in percentiles:
		color = getHex(getRed(per), getGreen(per), getBlue(per))
		colors.append(color)

	#assign color strings back to appropriate key in dictionary
	values = {}
	i = 0
	for key in dictFreq:
		count = dictFreq[key]
		values[colors[i]] = count
		dictFreq[key] = colors[i]
		i = i + 1
	
	#make sure every key accounted for
	values["#c445c4"]=0
	for char in validChars:
		if char not in dictFreq:
			dictFreq[char] = "#c445c4"

	return dictFreq, values

""" Draw each key """
def drawKeyboard(canvas, dictFreq):
	gap = 10
	halfLen = 15
	smallLen = 26
	normLen = 30
	tabLen = 35
	backLen = 40
	midLen = 50
	enterLen = 60
	longLen = 75
	longerLen = normLen * 2 + gap
	spaceLen = 200
	offx = 15
	offy = 17


	order = ["esc", "f1", "f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12", "prtsc", "insert", "delete", "play", "rewind", "fastforward", "off","`", "1","2","3","4","5","6","7","8","9","0","-","=", "backspace", "num lock","/","*","-","tab", "Q","W","E","R","T","Y","U","I","O","P","[","]","\\", "7", "8", "9", "+","caps","A","S","D","F","G","H","J","K","L",";","'","enter", "4", "5", "6","shift","Z","X","C","V","B","N","M",",",".","/", "shift", "1", "2", "3", "ctrl", "windows", " ","left","up","down","right"]
	index = 0
	global values
	colorDict, values = setColors(dictFreq, order)

	#esc, F keys, etc on top row
	#index = 0 to 19
	for i in range(20):
		x = 5 + gap * (i+1) + smallLen * i
		y = gap 
		if i not in [0,19]:
			canvas.create_rectangle(x, y, x+smallLen, y+halfLen, fill=colorDict[order[index]])
			canvas.create_text(x+offx+2,y+7,text=order[index])
			storeBox(x,y,x+smallLen, y+halfLen, colorDict[order[index]])
			index = index + 1
		else:
			canvas.create_rectangle(x, y, x+smallLen, y+halfLen, fill="gray")
			canvas.create_text(x+offx+2,y+7,text=order[index])
			index = index + 1



	#second row, with the numbers until backspace
	#index = 20 to 32
	for i in range(13):
		x = gap * (i+1) + normLen * i
		y = gap + normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#backspace, index = 33
	x = gap * 14 + normLen * 13
	y = gap + normLen
	canvas.create_rectangle(x, y, x+backLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+backLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#second row right side (after backspace)
	#index = 34 to 37
	for i in range(14,18):
		x = gap * (i+1) + normLen * (i-1) + backLen
		y = gap + normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		t = order[index]
		if t=="num lock":
			t = "num\nlock"
		canvas.create_text(x+offx,y+offy,text=t)
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1



	#third row tab
	#index = 38
	x = gap
	y = 2 * gap + 2 * normLen
	canvas.create_rectangle(x, y, x+tabLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+tabLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#third row until |
	#index = 39 to 50
	for i in range(12):
		x = (gap + tabLen) + gap * (i+1) + normLen * i
		y = 2 * gap + 2 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#|, index = 51
	x = (gap + tabLen) + gap * 13 + normLen * 12
	y = 2 * gap + 2 * normLen
	canvas.create_rectangle(x, y, x+tabLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+tabLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#third row right side (|)
	#index = 52 to 54
	for i in range(13,16):
		x = (gap + tabLen) + gap * (i+1) + normLen * (i-1) + tabLen
		y = 2 * gap + 2 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#third row (+), index = 55
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+longerLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+normLen, y+longerLen, colorDict[order[index]])
	index = index + 1
		


	#fourth row caps
	#index = 56
	x = gap
	y = 3 * gap + 3 * normLen
	canvas.create_rectangle(x, y, x+midLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+midLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fourth row until enter
	#index = 57 to 67
	for i in range(11):
		x = (gap + midLen) + gap * (i+1) + normLen * i
		y = 3 * gap + 3 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#enter, index = 68
	x = (gap + midLen) + gap * 12 + normLen * 11
	y = 3 * gap + 3 * normLen
	canvas.create_rectangle(x, y, x+enterLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+enterLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fourth row right side (after enter)
	#index = 69 to 71
	for i in range(12,15):
		x = (gap + midLen) + gap * (i+1) + normLen * (i-1) + enterLen
		y = 3 * gap + 3 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1



	#fifth row shift, index 72
	x = gap
	y = 4 * gap + 4 * normLen
	canvas.create_rectangle(x, y, x+longLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+longLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fifth row until shift
	#index = 73 to 82
	for i in range(10):
		x = (gap + longLen) + gap * (i+1) + normLen * i
		y = 4 * gap + 4 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#shift, index = 83
	x = (gap + longLen) + gap * 11 + normLen * 10
	y = 4 * gap + 4 * normLen
	canvas.create_rectangle(x, y, x+longLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+longLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fifth row right side (after shift)
	#index = 84 to 86
	for i in range(11,14):
		x = (gap + longLen) + gap * (i+1) + normLen * (i-1) + longLen
		y = 4 * gap + 4 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#fifth row enter, index = 87
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+longerLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+normLen, y+longerLen, colorDict[order[index]])
	index = index + 1
	



	#last row first keys
	#index = 88 to 91
	for i in range(4):
		x = gap * (i+1) + normLen * i
		y = 5 * gap + 5 * normLen
		fill = "gray"
		if i == 0:
			canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])	
			canvas.create_text(x+offx,y+offy,text=order[index])
			storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
			index = index + 1
		else:
			canvas.create_rectangle(x, y, x+normLen, y+normLen, fill="gray")
	#space bar, index = 92
	x = gap * 5 + normLen * 4
	y = 5 * gap + 5 * normLen
	canvas.create_rectangle(x, y, x+spaceLen, y+normLen, fill=colorDict[order[index]])
	storeBox(x,y,x+spaceLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#alt ctrl, index = 93 to 94
	x = gap * 6 + normLen * 4 + spaceLen
	y = 5 * gap + 5 * normLen
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill="gray")
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict["ctrl"])
	storeBox(x,y,x+normLen, y+normLen,colorDict["ctrl"])
	canvas.create_text(x+offx,y+offy,text="ctrl")
	#arrow, index = 95 to 98	
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
	storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
	index = index + 1
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+halfLen, fill=colorDict[order[index]])	
	storeBox(x,y,x+normLen, y+halfLen, colorDict[order[index]])
	index = index + 1
	canvas.create_rectangle(x, y+halfLen, x+normLen, y+normLen, fill=colorDict[order[index]])	
	storeBox(x,y,x+normLen, y+halfLen, colorDict[order[index]])
	index = index + 1
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
	storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#0, delete, index = 99, 100
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+2*normLen+gap, y+normLen, fill=colorDict["0"])
	storeBox(x,y,x+2*normLen+gap, y+normLen, colorDict["0"])
	canvas.create_text(x+offx,y+offy,text="0")
	x = x + 2*normLen + 2*gap
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict["delete"])
	canvas.create_text(x+offx,y+offy,text="delete")
	storeBox(x,y,x+normLen, y+normLen, colorDict["delete"])

	rectId = canvas.create_rectangle(-10,122,20,132,fill="#a6a832")
	labelId = canvas.create_text(-10,122,text="hi")
	canvas.bind("<Motion>", lambda event,canvas=canvas,labelId=labelId,rectId=rectId: hover(event,canvas, labelId, rectId))
	
