boxes = []
values = {}

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

def storeBox(x,y,x2,y2,color):
	global boxes 
	boxes.append([x,y,x2,y2,color])

def getBoxCount(x,y):
	global values
	for box in boxes:
		if x > box[0] and x < box[2] and y > box[1] and y < box[3]:
			#use color to get count
			return values[box[4]]
	return "NA"

def getRed(per):
	#colors bounce between 69 and 196, each color is 20 percents long
	step = (196 - 69)/ 20
	if per < 20:
		return 196 - step * per
	if per >=20 and per < 60:
		return 69
	if per >=60 and per < 80:
		return 69 + step * (per - 60)
	return 196

def getGreen(per):
	#colors bounce between 69 and 196, each color is 20 percents long
	step = (196 - 69)/ 20
	if per < 20:
		return 69
	if per >= 20 and per < 40:
		return 69 + (per - 20) * step
	if per >= 40 and per < 80:
		return 196
	return 196 - (per - 80) * step

def getBlue(per):
	#colors bounce between 69 and 196, each color is 20 percents long
	step = (196 - 69)/ 20
	if per < 40:
		return 196
	if per >= 40 and per < 60:
		return 196 - (per - 40) * step
	return 69

def getHex(r,g,b):
	hr = hex(int(r))[2:]
	hg = hex(int(g))[2:]
	hb = hex(int(b))[2:]
	return "#" + hr+hg+hb

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


	#can only list each key once since dictionary
	order = ["esc", "insert", "prtsc", "delete", "play", "rewind", "fast forward","`", "1","2","3","4","5","6","7","8","9","0","-","=", "back", "num lock","/","*","-","tab", "Q","W","E","R","T","Y","U","I","O","P","[","]","\\","+","caps","A","S","D","F","G","H","J","K","L",";","'","enter","shift","Z","X","C","V","B","N","M",",",".","/", "ctrl"," ","left","up","down","right"]
	index = 0
	global values
	colorDict, values = setColors(dictFreq, order)

	#esc, F keys, etc on top row
	for i in range(20):
		x = 5 + gap * (i+1) + smallLen * i
		y = gap 
		if i in [0,13,14,15,16,17,18]:
			canvas.create_rectangle(x, y, x+smallLen, y+halfLen, fill=colorDict[order[index]])
			canvas.create_text(x+offx+2,y+7,text=order[index])
			storeBox(x,y,x+smallLen, y+halfLen, colorDict[order[index]])
			index = index + 1
		else:
			canvas.create_rectangle(x, y, x+smallLen, y+halfLen, fill="gray")



	#second row, with the numbers until backspace
	for i in range(13):
		x = gap * (i+1) + normLen * i
		y = gap + normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#backspace
	x = gap * 14 + normLen * 13
	y = gap + normLen
	canvas.create_rectangle(x, y, x+backLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+backLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#second row right side (after backspace)
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
	x = gap
	y = 2 * gap + 2 * normLen
	canvas.create_rectangle(x, y, x+tabLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+tabLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#third row until |
	for i in range(12):
		x = (gap + tabLen) + gap * (i+1) + normLen * i
		y = 2 * gap + 2 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#|
	x = (gap + tabLen) + gap * 13 + normLen * 12
	y = 2 * gap + 2 * normLen
	canvas.create_rectangle(x, y, x+tabLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+tabLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#third row right side (|)
	for i in range(13,16):
		x = (gap + tabLen) + gap * (i+1) + normLen * (i-1) + tabLen
		y = 2 * gap + 2 * normLen
		keys = ["7","8","9"]
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[keys[i-13]])
		canvas.create_text(x+offx,y+offy,text=keys[i-13])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
	#third row (+)
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+longerLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+normLen, y+longerLen, colorDict[order[index]])
	index = index + 1
		


	#fourth row caps
	x = gap
	y = 3 * gap + 3 * normLen
	canvas.create_rectangle(x, y, x+midLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+midLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fourth row until enter
	for i in range(11):
		x = (gap + midLen) + gap * (i+1) + normLen * i
		y = 3 * gap + 3 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#enter
	x = (gap + midLen) + gap * 12 + normLen * 11
	y = 3 * gap + 3 * normLen
	canvas.create_rectangle(x, y, x+enterLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+enterLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fourth row right side (after enter)
	for i in range(12,15):
		x = (gap + midLen) + gap * (i+1) + normLen * (i-1) + enterLen
		y = 3 * gap + 3 * normLen
		keys = ["4","5","6"]
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[keys[i-12]])
		canvas.create_text(x+offx,y+offy,text=keys[i-12])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])



	#fifth row shift
	x = gap
	y = 4 * gap + 4 * normLen
	canvas.create_rectangle(x, y, x+longLen, y+normLen, fill=colorDict[order[index]])
	canvas.create_text(x+offx,y+offy,text=order[index])
	storeBox(x,y,x+longLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#fifth row until shift
	for i in range(10):
		x = (gap + longLen) + gap * (i+1) + normLen * i
		y = 4 * gap + 4 * normLen
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[order[index]])
		canvas.create_text(x+offx,y+offy,text=order[index])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
		index = index + 1
	#shift
	x = (gap + longLen) + gap * 11 + normLen * 10
	y = 4 * gap + 4 * normLen
	canvas.create_rectangle(x, y, x+longLen, y+normLen, fill=colorDict["shift"])
	canvas.create_text(x+offx,y+offy,text="shift")
	storeBox(x,y,x+longLen, y+normLen, colorDict["shift"])
	#fifth row right side (after shift)
	for i in range(11,14):
		x = (gap + longLen) + gap * (i+1) + normLen * (i-1) + longLen
		y = 4 * gap + 4 * normLen
		keys = ["1","2","3"]
		canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict[keys[i-11]])
		canvas.create_text(x+offx,y+offy,text=keys[i-11])
		storeBox(x,y,x+normLen, y+normLen, colorDict[order[index]])
	#fifth row enter
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+longerLen, fill=colorDict["enter"])
	canvas.create_text(x+offx,y+offy,text="enter")
	storeBox(x,y,x+normLen, y+longerLen, colorDict[order[index]])
	



	#last row first keys
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
	#space bar
	x = gap * 5 + normLen * 4
	y = 5 * gap + 5 * normLen
	canvas.create_rectangle(x, y, x+spaceLen, y+normLen, fill=colorDict[order[index]])
	storeBox(x,y,x+spaceLen, y+normLen, colorDict[order[index]])
	index = index + 1
	#alt ctrl
	x = gap * 6 + normLen * 4 + spaceLen
	y = 5 * gap + 5 * normLen
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill="gray")
	x = x + normLen + gap
	canvas.create_rectangle(x, y, x+normLen, y+normLen, fill=colorDict["ctrl"])
	storeBox(x,y,x+normLen, y+normLen,colorDict["ctrl"])
	canvas.create_text(x+offx,y+offy,text="ctrl")
	#arrow	
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
	#0, delete
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
	
