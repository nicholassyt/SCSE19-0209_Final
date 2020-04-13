import json
import ast
import pymongo 
import re
import os, sys, subprocess
import dateutil.parser
from datetime import datetime
from operator import itemgetter
import scripts.mongo.parameters as parameters

#Declarations
schemaFilesFolder  = os.path.join(os.path.dirname(__file__), "schemas/")						#Modify this if the folder of the various schemas is modified
SCHEMAEXT = "_schema" + parameters.TXTEXT 														#Modify this if the naming convention of the various schemas is modified
queryTypeFile = schemaFilesFolder + "query_type" + parameters.TXTEXT							#Modify this if the name of the query type txt file is modified
countryFile = schemaFilesFolder + "countryList" + parameters.JSONEXT	

resultsFilesFolder  = os.path.join(os.path.dirname(__file__), "results/")						#Modify this if the folder for the results is modified
searchFileName = resultsFilesFolder + "search_results" + parameters.JSONEXT 					#Modify this to change the name of the query results file
findFileName = resultsFilesFolder + "find_results" + parameters.JSONEXT 						#Modify this to change the name of the query results file
distinctFileName = resultsFilesFolder + "distinct_results" + parameters.TXTEXT					#Modify this to change the name of the distinct results txt file
aggregateFileName = resultsFilesFolder + "aggregate_results" + parameters.JSONEXT				#Modify this to change the name of the aggregate results file
descriptionFileName = resultsFilesFolder+ "count" + parameters.TXTEXT							#Modify this to change the name of the descriptions file	
queryRegex = "^(\{|\[)(\s|.)+(\}|\])$"															#Matches a query 
isodateRegex = "\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)"		#Match a isodate
idField = "_id"

removeFromQuery = ["country"]

#########################################################################################The GUI code is defined here###################################################################################################################
def getCollectionNames(db):
	return db.list_collection_names()

def parseSearchTerm(searchTerm):														#Prompts the user to enter the search term
	if searchTerm.isdigit():
		searchTerm = ast.literal_eval(searchTerm)										#Convert numbers to python literals
	elif re.match(isodateRegex,searchTerm):
		searchTerm = dateutil.parser.parse(searchTerm)									#If search term matches a date format, it will be converted
	elif searchTerm == "Null" or searchTerm == "null":
		searchTerm = None
	return searchTerm	

def parseQueryCode(queryCode):
	if re.search(isodateRegex,queryCode):												#ISODates are not supported in typed queries
		return False
	elif re.match(queryRegex,queryCode):												#If query is correct it will return True
		return True
	else:
		return False
#########################################################################################The GUI code is defined here#####################################################################################################################

#########################################################################################The Schema access code is defined here###########################################################################################################

def getSchema(col):																		
	try:
		schemaList = [line.rstrip('\n') for line in open(schemaFilesFolder + col + SCHEMAEXT)]					#Return schema list based on the collection for display
	except:
		print(schemaFilesFolder + col + SCHEMAEXT + " is not present")
	return schemaList

def getQueryType(): 																							#Return query type list for display
	return getListFromFile(queryTypeFile)

def getCountryList():																							#Return country type list for display. It comes as a file with multiple dictionaries
	return getListOfDictsFromJSONFile(countryFile)

def getListFromFile(fileName):
	try:
		listFromFile = [line.rstrip('\n').lower() for line in open(fileName)] 									#Strip \n from lines in file and lowercase it. The lines are stored in a list
	except:
		print(fileName + " is not present")
	return listFromFile

def getListOfDictsFromJSONFile(fileName):																		#Get a list of dicts from a file
	try:
		with open(fileName, encoding='utf-8') as data:									
			listOfDicts = json.load(data)													
			data.close()
	except:
		print(fileName + " is not present")
	return listOfDicts
		
#########################################################################################The Schema access code is defined here###########################################################################################################

#########################################################################################The Printing code is defined here################################################################################################################
class dateTimeEncoder(json.JSONEncoder):													#Datetime encoder for the printing of datetime
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

def cursorParsing(cursor):
	jsonList = []																			#Declare empty string list
	if isinstance(cursor, int):
		return jsonList
	else:
		for line in cursor:
			if idField in line:
				del line[idField]															#Remove '_id' field as it is not required for viewing
				jsonList.append(json.dumps(line,cls=dateTimeEncoder))						#Add cursor results to the string list
			else:
				jsonList.append(json.dumps(line,cls=dateTimeEncoder))
	cursor.close()
	return jsonList
	
def printQueryToFile(findCursor):
	i = 0																					#Declare counter
	findList = cursorParsing(findCursor)													#Assign the parsed string list from the function to the local string list
	if findCursor.retrieved != 0:															#If the query does not have empty results
		with open(findFileName, 'a', encoding='utf-8') as f:								#'a' is used to append queries to the same json file, encoding required to print VERIS queries
			for line in findList:
				print (line, file = f, end ='')												#Print the line from the string list into the out file
				if i != len(findList)-1 :									
					print(',', file = f)
					i+=1					
			print(']', file = f)
		f.close() 																			#Close the file
	return findList
	#findCursor.close()																		#Close the Cursor object
	
def printDistinctToFile(List):
	with open(distinctFileName, 'w', encoding='utf-8') as f:								#Prints distinct results to a file
		for x in List:
			print(x, file = f)	
	f.close()

def printAggregateToFile(aggregateCursor):													#Print aggregate results to a file
	i = 0
	aggregateList = cursorParsing(aggregateCursor)
	with open(aggregateFileName, 'a', encoding='utf-8') as f:
		for line in aggregateList:
			print (line, file = f)
			if i != len(aggregateList)-1 :									
					print(',', file = f)
					i+=1
		print(']', file = f)
	f.close()
	return aggregateList
	
def printSearchToFile(searchList):
	i = 0																					#Declare counter
	if len(searchList) != 0:																#If the query does not have empty results
		with open(searchFileName, 'a', encoding='utf-8') as f:								#'a' is used to append queries to the same json file, encoding required to print VERIS queries
			for line in searchList:
				print (line, file = f, end ='')												#Print the line from the string list into the out file
				if i != len(searchList)-1 :									
					print(',', file = f)
					i+=1					
			print(']', file = f)
		f.close() 																			#Close the file

def openFolder():																			#Open the folder where the files are contained
    if sys.platform == "win32":
        os.startfile(getFolderName())
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, getFolderName()])

def getFolderName():
	return os.path.realpath(resultsFilesFolder)												#Returns the path of the results file folder
	
#########################################################################################The Printing code is defined here################################################################################################################

#########################################################################################The Query code is defined here###################################################################################################################
def findQuery(dbCollection,column,queryType,searchTerm):											
	isCompleted = False
	try:
		clearFileContents(findFileName)																#Clear file contents to allow writing to be done to the file
		prepareFile(findFileName)																	#Prepare the json file by first appending a '['
		query = getQuery(column,queryType.split()[0],parseSearchTerm(searchTerm)) 					#split is used to remove everything after the first whitespace. Only the relevant query type like $eq or $regex will remain.
		findCursor = dbCollection.find(query)														#Do the query and store the results as a Cursor object
		findList = printQueryToFile(findCursor)														#The findCursor is parsed and a list of results is returned
		openFolder()
		isCompleted = True
		return isCompleted, findList
	except:
		return isCompleted

def findAndQuery(dbCollection,column,queryType,searchTerm,column2,queryType2,searchTerm2):			#An AND query has two query terms
	isCompleted = False
	try:
		clearFileContents(findFileName)																#Clear file contents to allow writing to be done to the file
		prepareFile(findFileName)																	#Prepare the json file by first appending a '['
		query = { "$and": [ { column : { queryType.split()[0]: parseSearchTerm(searchTerm) } }, { column2: { queryType2.split()[0] : parseSearchTerm(searchTerm2) } } ] }	#split is used to remove everything after the first whitespace. Only the relevant query type like $eq or $regex will remain.
		findCursor = dbCollection.find(query)														#Do the query and store the results as a Cursor object
		findList = printQueryToFile(findCursor)														#The findCursor is parsed and a list of results is returned
		openFolder()
		isCompleted = True
		return isCompleted, findList
	except:
		return isCompleted	
	
def findTypedQuery(dbCollection,query):
	isCompleted = False
	try:
		if parseQueryCode(query):
			clearFileContents(findFileName)															#Clear file contents to allow writing to be done to the file
			prepareFile(findFileName)																#Prepare the json file by first appending a '['
			query = ast.literal_eval(query)															#A typed query has to parsed with ast.literal_eval
			findCursor = dbCollection.find(query)													#Do the query and store the results as a Cursor object
			findList = printQueryToFile(findCursor)													#The findCursor is parsed and a list of results is returned
			openFolder()			
			isCompleted = True
		return isCompleted, findList
	except:
		return isCompleted
	
def distinctQuery(dbCollection,column):
	distinctList = dbCollection.find().distinct(column)												#A distinct query returns the distinct values in a column
	if len(distinctList) >= 100:
		printDistinctToFile(distinctList)															#If there are more than 100 results, the results are saved in a file
	return distinctList
	
def aggregateQuery(dbCollection,query):																#A aggregate query provides the aggregation functionality
	isCompleted = False
	try:
		if parseQueryCode(query):																	#The query is matched against a query code regex
			clearFileContents(aggregateFileName)													#Clear file contents to allow writing to be done to the file
			prepareFile(aggregateFileName)															#Prepare the json file by first appending a '['
			aggregateCursor = dbCollection.aggregate(ast.literal_eval((query)))						#A typed query has to parsed with ast.literal_eval
			aggregateList = printAggregateToFile(aggregateCursor)									#The aggregateCursor is parsed and a list of results is returned
			openFolder()
			isCompleted = True
			return isCompleted, aggregateList
	except:
		return isCompleted

def searchQuery(dbCollection,collection,searchQuery):
	isCompleted = False
	searchList = []
	try:
		if searchQuery != "" or searchQuery == None:
			clearFileContents(searchFileName)															#Clear file contents to allow writing to be done to the file
			prepareFile(searchFileName)																	#Prepare the json file by first appending a '['
			if ':' in searchQuery:																		#A FIELD:TERM is provided as input
				searchList.extend(fieldAndTerm(searchQuery,dbCollection))
			if '-' in searchQuery:																		#A CVE is provided as input
				searchList.extend(cveSearch(searchQuery,dbCollection))
			if len(searchList) == 0:																	#If user entered column : value and there are no results
				searchQuery = re.sub(r'[^\w]', ' ', searchQuery)										#Remove symbols
				word_list = [x.strip() for x in searchQuery.split()]									#Split words and strip whitespace
				filtered_words = [word for word in word_list if word not in removeFromQuery]			#Remove stopwords
				if len(filtered_words) != 0:
					filtered_words = [w.lower() for w in filtered_words]								#Lower the case of all words in list
					if len(filtered_words) == 1:
						searchList.extend(singleWordSearch(filtered_words[0],dbCollection))				#If the typed search term is a single word or a single word after initial parsing
					else:		
						searchList.extend(multipleWordSearch(filtered_words,collection,dbCollection))	#If the typed search term has multiple words
					
					searchList = list(dict.fromkeys(searchList)) 										#Remove duplicates
			printSearchToFile(searchList)
			openFolder()
			isCompleted = True
			return isCompleted, searchList
	
	except Exception as e:
		print(e)
		return isCompleted, searchList	

def fieldAndTerm(searchQuery,dbCollection):																#Parsing FIELD:TERM that is provided as input	
	word_list = [x.strip() for x in searchQuery.split(':')]												#Split by ":"
	query = getQuery(word_list[0],"$eq",word_list[1])													#Element 0 is the field while Element 1 is the term
	searchCursor = dbCollection.find(query)																#Parses the find query and returns the searchCursor
	return cursorParsing(searchCursor)

def cveSearch(searchQuery,dbCollection):																#Parsing CVE provided as input
	query = getQuery("cve","$eq",searchQuery)															#Search is made on the CVE field
	searchCursor = dbCollection.find(query)																#Parses the find query and returns the searchCursor
	return cursorParsing(searchCursor)

def singleWordSearch(singleWord,dbCollection):															#If the search term is a single word
	searchList = []
	countryList = getCountryList()																		
	
	for dict in countryList:																			#Matches the single term against the country or country codes
		if singleWord.upper() == dict["Code"]:
			searchList.extend(doCountryQuery(dict["Code"],dbCollection))
			#searchCursor.close()
		elif singleWord == dict["Country"].lower():
			searchList.extend(doCountryQuery(dict["Code"],dbCollection))
	
	query = getQuery("$text","$search",singleWord)														#Search list will include terms that are present in the text index
	searchCursor = dbCollection.find(query)
	searchList.extend(cursorParsing(searchCursor))
	return searchList

def doCountryQuery(countryCode,dbCollection):															#Both country and attacker.origin have country codes
	searchList = []
	query = getQuery("country","$eq",countryCode)
	searchCursor = dbCollection.find(query)																#Do the query and store the results as a Cursor object
	searchList.extend(cursorParsing(searchCursor))														#Return results List	
	query = getQuery("attacker.origin","$eq",countryCode)
	searchCursor = dbCollection.find(query)																#Do the query and store the results as a Cursor object
	searchList.extend(cursorParsing(searchCursor))														#Return results List
	return searchList

def multipleWordSearch(filtered_words,collection,dbCollection):
	searchList = []
	#For iterating
	monetaryIterationList = ["monetary","money","moneys"]
	attackerIterationList = ["name","origin","role"]
	targetIterationList = ["target","targeted","records","assets"]
	#For stemming
	attackStemming = ["attack","atk","attackers"]
	
	for word in filtered_words:
		if word in attackStemming:																		#Remove words related to attacker to allow for a standard attacker
			filtered_words.remove(word)
			filtered_words.append("attacker")
	
	for word in filtered_words:
		if word in monetaryIterationList:																#If the search term contains money, a search should be made on monetary_loss.amount
			columnToSearch = "monetary_loss.amount"
		elif word in attackerIterationList and "attacker" in filtered_words:							#If the search term contains attacker, a search should be made on attacker
			columnToSearch = "attacker.%s" % (word)
		elif "attacker" in filtered_words:																
			columnToSearch = "attacker.%s" % (attackerIterationList[0])
		elif word in targetIterationList:																#If the search term contains target, a search should be made on target
			if word == targetIterationList[0] or  word == targetIterationList[1]:
				columnToSearch = "target.targeted"
			else:
				word = word + "_affected"
				columnToSearch = "target.%s" % (word)
	
	for word in filtered_words:
		if "most" in filtered_words and ("loss" in filtered_words or "affected" in filtered_words):		#If the search term contains most and loss, a search should be made on monetary_loss.amount, ordered by the most montary loss
			if "records" in filtered_words or "record" in filtered_words:								#If records, sort by descending 
				searchList.extend(cursorParsing(dbCollection.find(getQuery("target.records_affected","$gte",0)).sort("target.records_affected",pymongo.DESCENDING)))
				break
			for mon in monetaryIterationList:															#If monetary, sort by descending 
				if mon in filtered_words:
					searchList.extend(cursorParsing(dbCollection.find(getQuery("monetary_loss.amount","$gte",0)).sort("monetary_loss.amount",pymongo.DESCENDING)))
	
	if columnToSearch != None:																			
		for word in filtered_words:
			if word != columnToSearch:
				if word.isdigit():																						#If the word is a digit $gte can be used
					valueToSearch = int(word)
					searchList.extend(cursorParsing(dbCollection.find(getQuery(columnToSearch,"$gte",valueToSearch))))
				else:
					regToUse = re.compile(word, re.IGNORECASE)
					searchList.extend(cursorParsing(dbCollection.find(getQuery(columnToSearch,"$regex",regToUse))))		#Regex is used to match words
	
	if len(searchList) == 0:																							#If there are still no results, the text index is searched
		sep = " "
		searchList.extend(cursorParsing(dbCollection.find(getQuery("$text","$search",sep.join(filtered_words)))))
	
	return searchList

def getQuery(columnToSearch,mongoOp,valueToSearch):																		#A query can be created with this function
	query = { columnToSearch : { mongoOp :  valueToSearch} }
	return query
#########################################################################################The Query code is defined here###################################################################################################################