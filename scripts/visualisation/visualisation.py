import matplotlib
matplotlib.use('Agg')		#To prevent main thread not in loop error
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import math
import json
import re
from operator import itemgetter
import scripts.visualisation.graph_parameters as gp
import scripts.visualisation.imageLocation as il
import scripts.visualisation.multiplelines as ml

#Declarations for graph display
graphImage = il.getGraphImageLocation()

pd.options.display.float_format = '{:.2f}'.format																		#Format the dataframe numbers with two decimal places instead of exponential numbers
graphFontsize = gp.graphFontsize																						#Set the font size
graphFontcolour = gp.graphFontcolour																					#Set the font colour
millnames = ['',' Thousand',' Million',' Billion',' Trillion']
numtypes = ["int64","float64"]

needXYgraphTypeList = ["bar", "line", "scatter", "box", "violin"]
graphTypeList = ["bar", "line", "scatter", "box", "violin"]																#Graphs available to be plotted

paramFields = ["Graph Title :", "x Axis :", "y Axis :", "x Label :", "y Label :","y Lower Limit :","y Upper Limit :"]	#Parameters to be collected
#paramExamples = gp.paramExamples																						#Parameter examples

#########################################################################################The Data Frame Parsing code is defined here###################################################################################################################

def parseDataFrame(dataFrame,paramsList):
	if len(dataFrame.columns)  == 2 and dataFrame.columns[0] == 0:
		dataFrame.columns = [paramsList[1],paramsList[2]]																#Assign the x and y axis

#########################################################################################The Data Frame Parsing code is defined here###################################################################################################################

#########################################################################################The Graph Plotting code is defined here###################################################################################################################
def parseLargeNumbers(num):
	num = float(num)
	millidx = max(0,min(len(millnames)-1,int(math.floor(0 if num == 0 else math.log10(abs(num))/3))))
	return '{:.0f}{}'.format(num / 10**(3 * millidx), millnames[millidx])

def annotateBar(graph):
	for p in graph.patches:
		graph.annotate(parseLargeNumbers(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),		#Annotates the each bar of the graph with the corresponding value
			ha = "center", va = "center", fontsize = graphFontsize, color = graphFontcolour, xytext = (0, 20),
			textcoords="offset points")

def annotateGeneric(dataFrame,xAxis,yAxis):
	for row in dataFrame.itertuples(index = True, name = "Pandas"):												#Annotates the each plotted point of the graph with the corresponding value
		plt.text(getattr(row,xAxis), getattr(row,yAxis)+2,
			str(f'{getattr(row,yAxis):,}'), ha = "center", va = "center", fontsize = graphFontsize, color = graphFontcolour)

def labelsGeneric(graph,paramsList):
	graph.yaxis.set_major_formatter(ticker.EngFormatter())														#English formatter allows for the graph ticks to be displayed as 10K instead of 10000
	graph.set_title(paramsList[0])																				#Set the graph title
	plt.xlabel(paramsList[3])																					#Label the x axis
	plt.ylabel(paramsList[4])																					#Label the y axis
	plt.ylim(int(paramsList[5]), int(paramsList[6]))															#Set the lower limit and upper limit of the yaxis

#Set up the various plots
def doBarPlot(dataFrame,paramsList,ax):
	graph = sns.barplot(ax=ax, x = paramsList[1], y = paramsList[2], data = dataFrame)							#Bar plot formation with the corresponding x and y axis and dataframe
	labelsGeneric(graph,paramsList)
	annotateBar(graph)																							#Annotate the bar chart	
	
def doLinePlot(dataFrame,paramsList,ax):
	graph = sns.lineplot(ax=ax, x = paramsList[1], y = paramsList[2], data = dataFrame)							#Line plot formation with the corresponding x and y axis and dataframe
	labelsGeneric(graph,paramsList)																				
	annotateGeneric(dataFrame,paramsList[1],paramsList[2])														#Annotate the line chart

def doScatterPlot(dataFrame,paramsList):
	graph = sns.scatterplot(x = paramsList[1], y = paramsList[2], data = dataFrame)								#Scatter plot formation with the corresponding x and y axis and dataframe
	labelsGeneric(graph,paramsList)
	annotateGeneric(dataFrame,paramsList[1],paramsList[2])														#Annotate the scatter plot

def doBoxPlot(dataFrame,paramsList):
	graph = sns.boxplot(x = paramsList[1], y = paramsList[2], data = dataFrame)									#Box plot formation with the corresponding x and y axis and dataframe
	labelsGeneric(graph,paramsList)
	annotateGeneric(dataFrame,paramsList[1],paramsList[2])														#Annotate the box plot
	
def doViolinPlot(dataFrame,paramsList):
	graph = sns.violinplot(x = paramsList[1], y = paramsList[2], data = dataFrame)								#Violin plot formation with the corresponding x and y axis and dataframe
	labelsGeneric(graph,paramsList)
	annotateGeneric(dataFrame,paramsList[1],paramsList[2])														#Annotate the violin plot

def doMulLinePlot(dataFrame,paramsList,ax):
	#x is usually a year value and y can be a value like number of incidents, with a group by industry or other terms in the database
	#Declarations
	colNames = dataFrame.columns
	markers = ['x','o']#Labels can be either x or o
	i = 0
	doLog = False
	
	while i != len(colNames):
		sum = dataFrame[colNames[i]].sum()						#Sum values in column
		if sum > 5000:
			doLog = True
			sum = int(math.ceil(sum))							#Remove any decimal places
		limit = int(paramsList[7])
		if sum >= limit:										#If the sum exceeds the limit 
			if (i%2 == 0):
				sns.set_color_codes("pastel")					#Set alternate colours
				marker = markers[0]
			else:
				marker = markers[1]
				sns.set_color_codes("muted")					#Set alternate colours
			if (isinstance(sum,int)):
				label = "{:d} {:s}".format(sum,colNames[i])		#If the value is an integer
			else:
				label = "{:.2f} {:s}".format(sum,colNames[i])	#If the value is a numeric type that is not an interger 

			#Scatter plot formation with the corresponding x and y axis and dataframe
			graph = sns.scatterplot(ax=ax, x = dataFrame.index, y = colNames[i], data = dataFrame, label = label, s=100 , marker = marker)
		i+=1
	
	if (doLog):
		ax.set_yscale('log')									#Log is done if the values exceed 5000
	labelsMultiple(graph,paramsList)							#Set the graph labels
	plotLegend(ax)												#Plot the legend
	
def plotLegend(ax):
	handles, labels = ax.get_legend_handles_labels()
	labels, handles = sortTuple(zip(labels,handles), itemgetter(0)) 											#sort tuple by the first element which are labels
	plt.legend(handles, labels)

def sortTuple(l, key):
	convert = lambda text: int(text) if text.isdigit() else text	
	alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]							#Sort by the first digit in the string
	return zip(*sorted(l, key = alphanum_key))

def labelsMultiple(graph,paramsList):
	graph.yaxis.set_major_formatter(ticker.EngFormatter())														#English formatter allows for the graph ticks to be displayed as 10K instead of 10000
	graph.set_title(paramsList[0])																				#Set the graph title
	plt.xlabel(paramsList[1])																					#Label the x axis
	plt.ylabel(paramsList[2])																					#Label the y axis
	xLimL,xLimH = limitCheck(int(paramsList[3]),int(paramsList[4]))												#Check for limits that might be entered wrongly
	yLimL,yLimH = limitCheck(int(paramsList[5]),int(paramsList[6]))												#Check for limits that might be entered wrongly
	plt.xlim(xLimL,xLimH)																						#Set the lower limit and upper limit of the xaxis
	plt.ylim(yLimL,yLimH)																						#Set the lower limit and upper limit of the yaxis

def limitCheck(limL,limH):																						#Check for limits that might be entered wrongly
	if limL > limH:
		temp = limL
		limL = limH
		limH = temp
	return limL,limH

#########################################################################################The Graph Plotting code is defined here###################################################################################################################

def stringToDataFrame(inputString):
	return pd.DataFrame.from_records(json.loads(inputString))													#Parse input string to dataframe object

def parseMulLineData(inputString,predType,predTypeList):
	#Example of dictionary
	#from [{'tool': 'Extortion', 'counts': [{'count': 3, 'year': 2014}]}, {'tool': 'Script', 'counts': [{'count': 16, 'year': 2014}, {'count': 4, 'year': 2013}]}]
	#to {'Extortion': [0, 3, 0, 0],'Script': [4, 16, 0, 0]}
	yearList = ml.getYearList()
	return pd.DataFrame(ml.parseMulLineData(json.loads(inputString),predType,predTypeList),index=yearList)		#Changes the dataframe index to year for predefined queries

def doGraph(graphType,paramsList,inputString = None, predType = None, predTypeList = None):
	isComplete = False
	try:
		plt.figure()
		sns.set(style = gp.seaBornStyle)																	#Set the background of the graph
		fig, ax = plt.subplots(figsize=gp.graphDimensions)													#Set the dimensions of the graph
		if inputString != None:
			if graphType == "mulLine":
				dataFrame = parseMulLineData(inputString,predType,predTypeList)								#If the type is predefined
			else:
				dataFrame = stringToDataFrame(inputString)
		if graphType in needXYgraphTypeList:
			parseDataFrame(dataFrame,paramsList)
		if graphType == "bar":																				#If type of graph parameter is a Barplot
			doBarPlot(dataFrame,paramsList,ax)
		elif graphType == "line":																			#If type of graph parameter is a Lineplot
			doLinePlot(dataFrame,paramsList,ax)
		elif graphType == "scatter":																		#If type of graph parameter is a Scatterplot
			doScatterPlot(dataFrame,paramsList)
		elif graphType == "box":																			#If type of graph parameter is a Boxplot
			doBoxPlot(dataFrame,paramsList)
		elif graphType == "violin":																			#If type of graph parameter is a Violinplot
			doViolinPlot(dataFrame,paramsList)
		elif graphType == "mulLine":																		#If parameter is a Predefined query	
			doMulLinePlot(dataFrame,paramsList,ax)
		plt.savefig(graphImage)																				#Save graph image to folder
		plt.close("all")																					#Closes all plots
		isComplete = True
		return isComplete
	except Exception as e:
		print(e)
		return isComplete