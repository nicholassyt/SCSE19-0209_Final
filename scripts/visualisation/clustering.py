import matplotlib
matplotlib.use('Agg')		#To prevent main thread not in loop error
import json
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing 
from sklearn.cluster import KMeans
import scripts.visualisation.imageLocation as il

jsonFile = il.getClusteringJSONFile()
elbowImage = il.getElbowImageLocation()
clusteringImage = il.getClusteringImageLocation()
mapFile = il.getMappingFile()
x = "x"
y = "y"
z = "z"
count = "count"
#numOfClusters = 4
numToFilter = 10
xLimitLower = 0
xLimitHigher = 100
yLimitLower = 0
yLimitHigher = 50

def doClustering(numOfClusters,clus,inputString):
	plt.figure()										# Clear the plot
	le = preprocessing.LabelEncoder() 					# Declare label_encoder object that will understand word labels. 

	df = pd.DataFrame(parseListOfDicts(inputString))	# Get dataframe from data
	
	# print(df.info())
	# print(df)
	
	df[x] = le.fit_transform(df[x]) # Encode labels in column
	df[y] = le.fit_transform(df[y]) # Encode labels in column
	#df.sort_values(by = [x], ascending=True, inplace=True)		#[y,x]
	# print(df.info())
	# print(df)
	if clus is False:
		saveElbow(df) 									#Call this if there is a need to check the number of clusters
	if clus is True:
		saveClustering(df,numOfClusters)				#Do Kmeans based on the number clusters that have been input

def saveClustering(df,numOfClusters):
	if numOfClusters != 0 or numOfClusters != None:
		#df = filterNumOfElements(df,y,numToFilter) 
		kmeans = KMeans(init='k-means++', n_clusters = numOfClusters)	#Create k means model
		kmeans.fit(df)													#Fit kmeans model
		labels = kmeans.predict(df)										#Predict with model against dataframe
		centroids = kmeans.cluster_centers_								#Store the centroids from the kmeans model into a variable
		
		plt.scatter(df[x], df[y], c=labels, s=50, cmap='viridis')		#Plot the scatter plot
		for idx, centroid in enumerate(centroids):						#Increas the size of and colour the centroids
			plt.scatter(*centroid, color='#050505', s=100, alpha = 0.5)	
		
		#showCountOfDF(df,y)
		#showMapping(df,le)
		#saveToFileConsolePrint(df,le,y)
		
		plt.xlim(xLimitLower, xLimitHigher)								#Limit the x axis
		plt.ylim(yLimitLower, yLimitHigher)								#Limit the y axis
		
		plt.savefig(clusteringImage)									#Save scatter plot
		#plt.show()

def saveElbow(df):														#Iterate the kmeans model 10 times to obtain the elbow graph
	wcss = []
	for i in range(1, 11):												
		kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)	
		kmeans.fit(df)
		wcss.append(kmeans.inertia_)
	plt.plot(range(1, 11), wcss)
	plt.title('Elbow Method')
	plt.xlabel('Number of clusters')
	plt.ylabel('WCSS')
	plt.savefig(elbowImage)

def saveToFileConsolePrint(df,le,y):												#Can be called to save the console printout for debugging
	f = open(mapFile, 'w')
	sys.stdout = f
	showMapping(df,le)
	showCountOfDF(df,y)
	f.close()

def showMapping(df,le):
	mapping = dict(zip(le.classes_, range(0, len(le.classes_))))					#Can be called to print the mapping from the labelling
	print(mapping)
	
def showCountOfDF(df,colName):
	df[count] = df.groupby(colName)[colName].transform(count)						#Can be called to count of values
	printall(df)

def filterNumOfElements(df,colName,filterNum):
	return df[df.groupby(colName)[colName].transform(count)>filterNum].copy()		#Can be called to filter the number of elements

def printall(df):
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):  #Printing a datafrome with the specified options
		print(df)

def getX(dict):
	return dict["entry_date"]["date"]												#X should be an input by the user
	
def getY(dict):
	return dict['objectives']														#Y should be an input by the user

def getZ(dict):
	return dict['unauthorized_result']												#Z should be an input by the user

def formDicts(dict):																#Form dictionary to be parsed into a dataframe
	listOfDicts = []
	xValue = getX(dict)
	yValue = getY(dict)
	zValue = getZ(dict)
	if xValue != None and yValue != None and zValue != None:
		if isinstance(yValue,list) and isinstance(zValue,list):						#Might be a list of values
			for yv in yValue:
				for zv in zValue:
					formY = yv + '-' + zv											#Append values to form a singular variable
					makeDict = {x : xValue, y : formY}#, z : zValue}
					listOfDicts.append(makeDict)
		return listOfDicts

def getListOfDictFromJSONFile():													#JSON file is a list of dictionaries
	with open(jsonFile, 'r') as f:
		listOfDict = json.load(f)
	return listOfDict		
	
def stringToListOfDicts(inputString):												#Load the JSON object from the input string
	return json.loads(inputString)	

def parseListOfDicts(inputString):
	listOfDicts = stringToListOfDicts(inputString)									#Read from an input string  getListOfDictFromJSONFile() df = pd.read_json(jsonFile)
	parsedListOfDicts = []
	for dict in listOfDicts:
		parsedListOfDicts.extend(formDicts(dict))									#Each dictionary must be parsed to retrieve the relevant results
	return parsedListOfDicts