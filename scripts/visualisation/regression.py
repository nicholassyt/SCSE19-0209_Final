import matplotlib
matplotlib.use('Agg')		#To prevent main thread not in loop error
import json
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing 
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split 
import scripts.visualisation.imageLocation as il

#Declarations
jsonFile = il.getRegressionJSONFile()
mapFile = il.getMappingFile()
regressionImage = il.getRegressionImageLocation()
x = "x"
y = "y"
count = "count"

numToFilter = 10
xLimitLower = 0
xLimitHigher = 800
yLimitLower = 0
yLimitHigher = 1000000

def doRegression(inputString):
	plt.figure()													#Clear the plot
	le = preprocessing.LabelEncoder() 								#Declare label_encoder object that will understand word labels. 
	reg = linear_model.LinearRegression()							#Create LinearRegression object
	
	df = pd.DataFrame(parseListOfDicts(inputString))				#Get dataframe
	df[x] = le.fit_transform(df[x]) # Encode labels in column
	#df[y] = le.fit_transform(df[y]) # Encode labels in column
	#df.sort_values(by = [y,x], ascending=True, inplace=True)		#[y,x]
	#print(df.info())
	#print(df)
	#df = filterNumOfElements(df,y,numToFilter) 
	
	X = df[x].values.reshape(-1,1)									#Values have to be reshaped to allow for regression
	Y = df[y].values.reshape(-1,1)
	
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)	#Split data into training and test sets

	reg.fit(X_train, Y_train)																	#Train model
	y_pred = reg.predict(X_test)																#Predict with test set
	
	concatX = np.concatenate((X_train,X_test),axis=None)										#Concat the x set
	concatY = np.concatenate((Y_train,Y_test),axis=None)										#Concat the y set
	plt.scatter(concatX, concatY,  color='black')												#Plot the linear regression scatter plot
	plt.plot(X_test, y_pred, color='red', linewidth=3)											#Colour the regression line red
	
	plt.xlim(xLimitLower, xLimitHigher)															#Set the limits of the xaxis
	plt.ylim(yLimitLower, yLimitHigher)															#Set the limits of the yaxis
	plt.savefig(regressionImage)																#Save scatter plot to file
	return getRegressionDetails(reg,Y_test,y_pred)
	#saveToFileConsolePrint(df,le,y,reg,Y_test,y_pred)											#Print regression details
	#plt.show()

def getRegressionDetails(reg,Y_test,y_pred):													#Return the regressions details for display in the interface
	termList = ["Intercept","Coefficients","Mean Absolute Error","Mean squared error","Coefficient of determination"]
	valueList = [reg.intercept_,reg.coef_,mean_absolute_error(Y_test, y_pred),mean_squared_error(Y_test, y_pred),r2_score(Y_test, y_pred)]
	termList.append("Intercept") 
	valueList.append(reg.intercept_)
	return termList,valueList
	
	# #The intercept
	# print("Intercept: %.2f" % reg.intercept_)
	
	# # The coefficients
	# print('Coefficients: %.2f' % reg.coef_)
	
	# # The mean absolute Error
	# print('Mean Absolute Error: %.2f' % mean_absolute_error(Y_test, y_pred)) 
	
	# # The mean squared error
	# print('Mean squared error: %.2f' % mean_squared_error(Y_test, y_pred))
	
	# # The coefficient of determination: 1 is perfect prediction
	# print('Coefficient of determination: %.2f' % r2_score(Y_test, y_pred))

# def printRegressionDetails(reg,Y_test,y_pred):
	# #The intercept
	# print("Intercept: %.2f" % reg.intercept_)
	
	# # The coefficients
	# print('Coefficients: %.2f' % reg.coef_)
	
	# # The mean absolute Error
	# print('Mean Absolute Error: %.2f' % mean_absolute_error(Y_test, y_pred)) 
	
	# # The mean squared error
	# print('Mean squared error: %.2f' % mean_squared_error(Y_test, y_pred))
	
	# # The coefficient of determination: 1 is perfect prediction
	# print('Coefficient of determination: %.2f' % r2_score(Y_test, y_pred))

def saveToFileConsolePrint(df,le,y,reg,Y_test,y_pred):												#Can be called to print regression details
	f = open(mapFile, 'w')
	sys.stdout = f
	printRegressionDetails(reg,Y_test,y_pred)
	showMapping(df,le)
	showCountOfDF(df,y)
	f.close()	

def showMapping(df,le):
	mapping = dict(zip(le.classes_, range(0, len(le.classes_))))									#Show the mapping of the labels
	print(mapping)
	
def showCountOfDF(df,colName):
	df[count] = df.groupby(colName)[colName].transform(count)										#Show the count in the dataframe
	printall(df)

def filterNumOfElements(df,colName,filterNum):
	return df[df.groupby(colName)[colName].transform(count)>filterNum].copy()						#Filter number of elements

def printall(df):
	with pd.option_context('display.max_rows', None, 'display.max_columns', None): 					#Printing a datafrome with the specified options
		print(df)

def getX(dict):
	return dict["entry_date"]["date"]																#X should be an input by the user
	
# def getY(dict):
	# ra = dict["target"]["records_affected"]
	# if ra != None: #and ra <= 4500000:
		# return ra
	# else:
		# return 0

def getY(dict):																						#Y should be an input by the user
	if "monetary_loss" in dict and dict["monetary_loss"] != None:
		ml = dict["monetary_loss"]["amount"]
		if ml != None: #and ra <= 4500000:
			return ml
	else:
		return 0		

def formDicts(dict):																				#Form dictionary to be parsed into a dataframe
	listOfDicts = []
	xValue = getX(dict)
	yValue = getY(dict)
	if yValue != None:
		makeDict = {x : xValue, y : yValue}
		listOfDicts.append(makeDict)
	return listOfDicts

def getListOfDictFromJSONFile():																	#JSON file is a list of dictionaries
	with open(jsonFile, 'r') as f:
		listOfDict = json.load(f)
	return listOfDict	

def stringToListOfDicts(inputString):																#Load the JSON object from the input string
	return json.loads(inputString)

def parseListOfDicts(inputString):
	listOfDicts = stringToListOfDicts(inputString)													#Read from an input stringgetListOfDictFromJSONFile()		#df = pd.read_json(jsonFile)
	parsedListOfDicts = []
	for dict in listOfDicts:
		parsedListOfDicts.extend(formDicts(dict))													#Each dictionary must be parsed to retrieve the relevant results
	return parsedListOfDicts