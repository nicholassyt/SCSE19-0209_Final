import json
import ast
import pymongo 
import scripts.mongo.parameters as parameters
#import parameters as parameters
import re
from datetime import datetime
import os, sys, subprocess
import dateutil.parser

#Declarations
schemaFilesFolder  = os.path.join(os.path.dirname(__file__), "schemas/")						#Modify this if the folder of the various schemas is modified
SCHEMAEXT = "_schema" + parameters.TXTEXT 														#Modify this if the naming convention of the various schemas is modified
queryTypeFile = schemaFilesFolder + "query_type" + parameters.TXTEXT							#Modify this if the name of the query type txt file is modified
toolListFile = schemaFilesFolder + "tool_list" + parameters.TXTEXT	
industryListFile = schemaFilesFolder + "industry_list" + parameters.TXTEXT	
objectivesListFile = schemaFilesFolder + "objectives_list" + parameters.TXTEXT	
unAuthListFile = schemaFilesFolder + "unauthorized_result_list" + parameters.TXTEXT	

resultsFilesFolder  = os.path.join(os.path.dirname(__file__), "results/")						#Modify this if the folder for the results is modified
aggregateFileName = resultsFilesFolder + "multiple_aggregate_results" + parameters.JSONEXT		#Modify this to change the name of the aggregate results file

queryRegex = "^(\{|\[)(\s|.)+(\}|\])$"															#Matches a query 
isodateRegex = "\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)"		#Match a isodate
idField = "_id"

predTypeList = ["Overall Tool count by Year","Specific Tool count by selected Industries","Specific Industry count by selected Tools","Monetary loss by selected Industries","Monetary loss by selected Tools","Monetary loss by specific Industry and selected Tools","Monetary loss by specific Tool and selected Industries","Records affected by selected Industries","Records affected by selected Tools","Records affected by specific industry and selected Tools","Records affected by specific Tool and selected Industries","Overall Objectives count by Year","Specific Objective count by selected Industries","Specific Industry count by selected Objectives","Overall Unauthorized Result count by Year","Specific Unauthorized Result count by selected Industries","Specific Industry count by selected Unauthorized Results"]

#########################################################################################The GUI code is defined here###################################################################################################################
def getCollectionNames(db):
	return db.list_collection_names()													#Returns the list of collections in the database

def parseSearchTerm(searchTerm):														#Prompts the user to enter the search term
	if searchTerm.isdigit():
		searchTerm = ast.literal_eval(searchTerm)										#Convert numbers to python literals
	elif re.match(isodateRegex,searchTerm):
		searchTerm = dateutil.parser.parse(searchTerm)									#If a date is matched, convert it to datetime
	return searchTerm	

def parseQueryCode(queryCode):
	if re.search(isodateRegex,queryCode):												#ISODates are not supported in typed queries and will return False
		return False
	elif re.match(queryRegex,queryCode):												#If query is correct it will return True
		return True
	else:
		return False
#########################################################################################The GUI code is defined here#####################################################################################################################

#########################################################################################The Schema access code is defined here###########################################################################################################

def openSchema(col):																		
	schemaList = [line.rstrip('\n') for line in open(schemaFilesFolder + col + SCHEMAEXT)]				#Returns schema list for display
	return schemaList
	
def openQueryType():
	QueryTypeList = [line.rstrip('\n') for line in open(queryTypeFile)]									#Returns query type list for display
	return QueryTypeList
	
def getToolList():
	toolList = [line.rstrip('\n') for line in open(toolListFile)]										#Returns tool list for display
	return toolList
	
def getIndustryList():
	industryList = [line.rstrip('\n') for line in open(industryListFile)]								#Returns industry list for display
	return industryList
	
def getPredTypeList():																					#Returns predefined type list for display
	return predTypeList
	
def getObjectivesList():
	objectivesList = [line.rstrip('\n') for line in open(objectivesListFile)]							#Returns objectives list for display
	return objectivesList
	
def getUnAuthList():
	unAuthList = [line.rstrip('\n') for line in open(unAuthListFile)]									#Returns unauthorised results list for display
	return unAuthList
		
#########################################################################################The Schema access code is defined here###########################################################################################################

#########################################################################################The Printing code is defined here################################################################################################################
class dateTimeEncoder(json.JSONEncoder):													#date time encoder for printing of datetime results
	def default(self, obj):
		if isinstance (obj, datetime): 
			return str(obj.isoformat())
		elif isinstance (obj, datetime.date):
			return str(obj.isoformat())
		return json.JSONEncoder.default(self, obj)

def clearFileContents(fileName):															#Function to clear file contents
	open(fileName, 'w').close()

def prepareFile(fileName):
	with open(fileName, 'a', encoding='utf-8') as f:	
		print('[', file = f)																#Append a '['
	f.close()

def cursorParsing(findCursor):
	jsonList = []																			#Declare empty string list
	for line in findCursor:
		if idField in line:
			del line[idField]																#Remove '_id' field as it is not required for viewing
			jsonList.append(json.dumps(line,cls=dateTimeEncoder))							#Add cursor results to the string list
		else:
			jsonList.append(json.dumps(line,cls=dateTimeEncoder))							
	return jsonList

def openFolder():																			#For the opening of the folder after the file has been created
    if sys.platform == "win32":
        os.startfile(getFolderName())
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, getFolderName()])

def getFolderName():																		#Results folder
	return os.path.realpath(resultsFilesFolder)
	
#########################################################################################The Printing code is defined here################################################################################################################

#########################################################################################The Query code is defined here###################################################################################################################

def printMulAggregateToFile(printList):														#Print the results of a multiple aggregate to the file
	clearFileContents(aggregateFileName)
	prepareFile(aggregateFileName)
	i = 0
	with open(aggregateFileName, 'a', encoding='utf-8') as f:
		for line in printList:
			print (json.dumps(line), file = f)
			if i != len(printList)-1 :									
				print(',', file = f)
				i+=1
		print(']', file = f)
	f.close()

def queryMul(dbCollection,aggregateString,predType,industry = None,toolName = None,objective = None, unauthorizedResult = None):	#Do an aggregate query with multiple variables
	aggregateCursor = dbCollection.aggregate(ast.literal_eval((aggregateString)))													#Results are returned as a cursor
	aggregateStringList = cursorParsing(aggregateCursor)																			#Parses the aggregate query result
	aggregateList = []
	aggregateDict = None
	for line in aggregateStringList:
		aggregateList.append(ast.literal_eval(line))																				#Each line in the string list is a actually a dict and this is converted with ast.literal_eval
	if len(aggregateList) >= 1:																										#The aggregate dictionary is formed with the aggregated list of dicts
		aggregateDict = {"Predefine" : predType, "industry" : industry, "tool" : toolName, "objectives" : objective , "unauthorized_result" : unauthorizedResult, "aggregateList" : aggregateList}
	aggregateCursor.close()
	if aggregateDict != None:
		return aggregateDict

#########################################################################################The Query code is defined here###################################################################################################################

def doPreDQuery(dbCollection, predList):
	isCompleted = False
	#The valuess are obtained from the user interface 
	predType = predList[0]
	startYear = predList[1]
	industry = predList[2]
	industryList = predList[3]
	tool = predList[4]
	toolList = predList[5]
	objective = predList[6]
	objectivesList = predList[7]
	unAuth = predList[8]
	unAuthList = predList[9]
	resultList = []
	
	#Each switch is a aggregate query. The function of each query can be referenced from the predTypeList list above.
	try:
		if predType == predTypeList[0]:
			for toolName in toolList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + toolName + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType, toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
	
		elif predType == predTypeList[1]:
			for ind in industryList:
				aggregateString = "[{ \"$match\" : { \"industry\" : { \"$eq\": \"" + ind + "\" },\"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + tool + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind, toolName = tool)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[2]:
			for toolName in toolList:
				aggregateString = "[{ \"$match\" : { \"industry\" : { \"$eq\": \"" + industry + "\" },\"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + toolName + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = industry,toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[3]: #"Monetary loss by selected Industries"
			for ind in industryList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + ind + "\" },\"monetary_loss.currency\": {\"$eq\": \"USD\" },\"monetary_loss.isEstimate\" : { \"$eq\": \"No\" },}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"lossAmt\" : { \"$sum\" : { \"$sum\" : \"$monetary_loss.amount\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"lossAmt\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[4]: #"Monetary loss by selected Tools"
			for toolName in toolList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + toolName + "\" },\"monetary_loss.currency\": {\"$eq\": \"USD\" },\"monetary_loss.isEstimate\" : { \"$eq\": \"No\" },}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"lossAmt\" : { \"$sum\" : { \"$sum\" : \"$monetary_loss.amount\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"lossAmt\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[5]: #"Monetary loss by specific Industry and selected Tools"
			for toolName in toolList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + toolName + "\" }, \"industry\" : {\"$eq\": \"" + industry + "\" },\"monetary_loss.currency\": {\"$eq\": \"USD\" },\"monetary_loss.isEstimate\" : { \"$eq\": \"No\" },}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"lossAmt\" : { \"$sum\" : { \"$sum\" : \"$monetary_loss.amount\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"lossAmt\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = industry, toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[6]: #"Monetary loss by specific Tool and selected Industries"
			for ind in industryList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + ind + "\" }, \"tool\" : {\"$eq\": \"" + tool + "\" },\"monetary_loss.currency\": {\"$eq\": \"USD\" },\"monetary_loss.isEstimate\" : { \"$eq\": \"No\" },}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"lossAmt\" : { \"$sum\" : { \"$sum\" : \"$monetary_loss.amount\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"lossAmt\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind,toolName = tool)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[7]:
			for ind in industryList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + ind + "\" }}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"dataRecords\" : { \"$sum\" : { \"$sum\" : \"$target.records_affected\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"dataRecords\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[8]:
			for toolName in toolList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"tool\" : {\"$eq\": \"" + toolName + "\" }}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"dataRecords\" : { \"$sum\" : { \"$sum\" : \"$target.records_affected\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"dataRecords\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[9]:
			for toolName in toolList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + industry + "\" }, \"tool\" : {\"$eq\": \"" + toolName + "\" }}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"dataRecords\" : { \"$sum\" : { \"$sum\" : \"$target.records_affected\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"dataRecords\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = industry, toolName = toolName)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[10]:
			for ind in industryList:
				aggregateString = "[{\"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + ind + "\" }, \"tool\" : {\"$eq\": \"" + tool + "\" }}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"dataRecords\" : { \"$sum\" : { \"$sum\" : \"$target.records_affected\"}},\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"dataRecords\" : 1,\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind,toolName = tool)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[11]:
			for obj in objectivesList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"objectives\" : {\"$eq\": \"" + obj + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,objective = obj)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[12]: #Specific Objectives count by selected Industries
			for ind in industryList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + ind + "\" }, \"objectives\" : {\"$eq\": \"" + objective + "\" }}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind,objective = objective)
				if aggDict != None:
					resultList.append(aggDict)
		
		elif predType == predTypeList[13]: #Specific Industry count by selected Objectives
			for obj in objectivesList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " },\"industry\" : {\"$eq\": \"" + industry + "\" }, \"objectives\" : {\"$eq\": \"" + obj + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = industry,objective = obj)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[14]: #Overall unauthorized_result count by Year
			for una in unAuthList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " }, \"unauthorized_result\" : {\"$eq\": \"" + una + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,unauthorizedResult = una)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[15]: #"Specific Unauthorized Result count by selected Industries"
			for ind in industryList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " }, \"industry\" : {\"$eq\": \"" + ind + "\" }, \"unauthorized_result\" : {\"$eq\": \"" + unAuth + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = ind,unauthorizedResult = unAuth)
				if aggDict != None:
					resultList.append(aggDict)
					
		elif predType == predTypeList[16]: #"Specific Industry count by selected Unauthorized Results"
			for una in unAuthList:
				aggregateString = "[{ \"$match\" : { \"entry_date.year\" : { \"$gte\" : " + str(startYear) + " }, \"industry\" : {\"$eq\": \"" + industry + "\" }, \"unauthorized_result\" : {\"$eq\": \"" + una + "\"}}},{\"$group\" : {\"_id\" : \"$entry_date.year\",\"count\" : { \"$sum\" : 1 }}},{\"$project\" :{\"_id\" : 0,\"year\" : \"$_id\",\"count\" : 1}},{\"$sort\" : { \"year\": -1 }}]"
				aggDict = queryMul(dbCollection,aggregateString,predType,industry = industry,unauthorizedResult = una)
				if aggDict != None:
					resultList.append(aggDict)			
		
		printMulAggregateToFile(resultList)						#Print the aggregated results to a file
		openFolder()
		isCompleted = True
		return isCompleted, resultList							#Return the results to create a multiple variable graph
	except Exception as e:
		print(e) 
		return isCompleted, resultList