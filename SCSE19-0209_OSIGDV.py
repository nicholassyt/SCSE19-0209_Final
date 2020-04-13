from flask import Flask, render_template, request, redirect, url_for
import sys
import json
import scripts.mergeSchema.merge as ms
import scripts.mongo.connectMongo as cm
import scripts.mongo.storeMongo as sm
import scripts.mongo.dropMongo as dm
import scripts.mongo.queryMongo as qm
import scripts.mongo.predMongo as pm
import scripts.visualisation.visualisation as vs
import scripts.visualisation.clustering as cl
import scripts.visualisation.regression as reg
import scripts.visualisation.imageLocation as il

#Declarations
app = Flask(__name__)
il.assignConfig(app)
hostURL = "0.0.0.0"
mainPage = "http://127.0.0.1:5000"
webTitle = "SCSE19-2019"
jsonLoaded = "JSON data has been loaded."
limit = 15
distinctLimit = 100
predTypeList = pm.getPredTypeList()

#Declarations for global values
thismodule = sys.modules[__name__]
thismodule.connectionType = None
thismodule.db = None
thismodule.collection = None 
thismodule.dbCollection = None 
thismodule.operation = None 
thismodule.jsonStr = []
thismodule.predType = None

#Parameters for a graph
exampleSingleParamList = ["Title","year","count","Year","Number Of Incidents","0","100"]
exampleMultiParamList = ["Title","Year","Number Of Incidents","2012","2019","0","10000","10"]

#Updates the global JSON string object so it is persistent 
def update_json(jsonVar):
	if jsonVar == None or jsonVar == []:
		jsonStr = ""
	elif isinstance(jsonVar[0], dict):			#If the variable is a list of dicts, convert it to JSON string object
		jsonStr = json.dumps(jsonVar)
	elif isinstance(jsonVar, list):
		jsonStr = '[' + ','.join(jsonVar) + ']' #If the variable it a list of strings, convert it to JSON string object
	else:	
		jsonStr = jsonVar						#If the variable it a JSON string
	thismodule.jsonStr = jsonStr				#Update the JSON string object 

def update_predType(predType):
  thismodule.predType = predType				#Updates the predefined type

def update_connection(ct,db):					#Updates the connection object
  thismodule.connectionType = ct
  thismodule.db = db
  
def update_collection(collection,operation):	#Updates the collection object and operation type
  thismodule.collection = collection
  thismodule.dbCollection = db[collection]
  thismodule.operation = operation
 
@app.after_request
def add_header(response):	#Disable caching which allows for images to be updated
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
  
@app.route('/')		#Index
@app.route('/index', methods = ['GET', 'POST'])
def index():
	return render_template('index.html', title = webTitle) #Returns the Index html

@app.route('/merge', methods = ['GET', 'POST'])	#Merge shows the merge
def merge():
	if request.method == 'POST':				#A POST request will call the merge function
		completed = ms.doMerge()				#Call the merge function
		if completed != False:					
			return render_template('merge.html', title = webTitle, JSONFiles = ms.getJSONFileNames(), isMerged = "merged as SCSE19_0209.json")		#Display the merged JSON
	#A get request will display the unmerged JSON files
	return render_template('merge.html', title = webTitle, JSONFiles = ms.getJSONFileNames(), isMerged = "not merged")	

@app.route('/mongo', methods = ['GET', 'POST'])			#Returns the mongoDB operations
def mongo():
	return render_template('mongo.html', title = webTitle, ct = connectionType) #pass variables to the html	

@app.route('/mongo/query', methods = ['GET', 'POST'])	#Returns the mongoDB query page
def query():
	colList = qm.getCollectionNames(db)
	return render_template('query.html', title = webTitle, len = len(colList), colList = colList) #pass variables to the html	

@app.route('/mongo/search', methods = ['GET', 'POST'])	#Returns the mongoDB search page
def search():
	colList = qm.getCollectionNames(db)
	return render_template('search.html', title = webTitle, len = len(colList), colList = colList) #pass variables to the html	

@app.route('/mongo/search/results', methods = ['POST'])	#Returns the mongoDB search results page
def searchResults():
	if request.method == 'POST':						#A POST request will call the search function
		collection = request.form["collectionToQuery"]	#Get the collection to query
		operation = "Search"				
		searchQuery = request.form["searchQuery"]		#Get the search term
		update_collection(collection,operation)			#Update the global values
		queryResult,jsonList = qm.searchQuery(dbCollection,collection,searchQuery)	#Call the search query function
		
		if queryResult and len(jsonList) >= 1:			#If there are results
			update_json(jsonList) 						#Update global jsonStr
			if len(jsonList) > limit:					#Limit results if the length exceeds the limit
				resultLength = limit
				displayResults = "You have searched for \"%s\". There are %d results but the first %d are displayed." % (searchQuery,len(jsonList),limit)		
			else:
				resultLength = len(jsonList)
				displayResults = "You have searched for \"%s\"" % (searchQuery)
			
			return render_template('queryResult.html', title = webTitle, len1 = resultLength, resultList = json.loads(jsonStr), displayResults = displayResults)	#Return results 
		else:
			return redirect(request.referrer, code = 302)	#Return the user to the search page if there are no results

@app.route('/mongo/query/select', methods = ['POST'])	#Redirects user after a query selection is made
def querySelect():
	if request.method == 'POST':						#A POST request will redirect the user to the appropriate page
		collection = request.form["collectionToQuery"]	#Get the collection to query
		operation = request.form["operation"]			#Get the operation
		update_collection(collection,operation)			#Update the global values
		if operation == "Find":							
			return redirect('/mongo/query/find')		#Redirect to find
		if operation == "Distinct":
			return redirect('/mongo/query/columns')		#Redirect to columns
		if operation == "Aggregate":
			return redirect('/mongo/query/aggregate')	#Redirect to aggregate
		if operation == "PreD":
			return redirect('/mongo/query/pred')		#Redirect to predefined
		return redirect('/mongo')				#If all conditions are not met, return the user to the selection page

@app.route('/mongo/query/find', methods = ['GET'])		#Returns the find page
def queryFind():
	columnList = qm.getSchema(collection)				#Get the schema list
	queryList = qm.getQueryType()						#Get the query types
	#The FIND template will be returned. If there has been an issue with the query, the error template will be returned.
	if request.method == 'GET' and request.headers['Referer'] == mainPage+url_for('query'):
		return render_template('queryFind.html', title = webTitle, len1 = len(columnList), columnList = columnList, len2 = len(queryList), queryList = queryList, error = "")
	else:
		return render_template('queryFind.html', title = webTitle, len1 = len(columnList), columnList = columnList, len2 = len(queryList), queryList = queryList, error = "There is an issue with the query.")

@app.route('/mongo/query/pred', methods = ['GET'])
def queryPreD():
	toolList = pm.getToolList()					#Get the tool list
	industryList = pm.getIndustryList()			#Get the industry list
	objectivesList = pm.getObjectivesList()		#Get the objectives list
	unAuthList = pm.getUnAuthList()				#Get the unauthorised list
	#The Search template will be returned. If there has been an issue with the query, the error template will be returned.
	if request.method == 'GET' and request.headers['Referer'] == mainPage+url_for('query'): 
		return render_template('queryPredefine.html', title = webTitle, len1 = len(predTypeList), predTypeList = predTypeList, len2 = len(toolList), toolList = toolList, len3 = len(industryList), industryList = industryList, len4 = len(objectivesList), objectivesList = objectivesList, len5 = len(unAuthList), unAuthList = unAuthList, error = "")
	else:
		return render_template('queryPredefine.html', title = webTitle, len1 = len(predTypeList), predTypeList = predTypeList, len2 = len(toolList), toolList = toolList, len3 = len(industryList), industryList = industryList, len4 = len(objectivesList), objectivesList = objectivesList, len5 = len(unAuthList), unAuthList = unAuthList, error = "There is an issue with the query.")

@app.route('/mongo/query/columns', methods = ['GET'])
def queryColumns():
	columnList = qm.getSchema(collection)			#Get the columns in the collection
	return render_template('queryColumns.html', title = webTitle, len = len(columnList), columnList = columnList, op = operation.lower())	#Return the columns to be selected

@app.route('/mongo/query/distinct', methods = ['POST'])
def queryDistinct():
	if request.method == 'POST':
		column = request.form["column"]							#Get the column
		distinctResults = qm.distinctQuery(dbCollection,column)	#Call the distinct query function

		if len(distinctResults) >= distinctLimit:				#If there are too many distinct results, limit the number of displayed results
			displayResults = "Distinct query has been made on \"%s\". There are %d results but the first %d are displayed. The results will be save in a file." % (column,len(distinctResults),distinctLimit)
			return render_template('queryDistinct.html', title = webTitle, column = column, len = distinctLimit, distinctResults = distinctResults, displayResults = displayResults)	
		else:
			displayResults = "You have searched for \"%s\". There are %d results." % (column,len(distinctResults))
			return render_template('queryDistinct.html', title = webTitle, column = column, len = len(distinctResults), distinctResults = distinctResults, displayResults = displayResults)	

@app.route('/mongo/query/aggregate', methods = ['GET'])
def queryAggregate():
	#The Aggregate template will be returned. If there has been an issue with the query, the error template will be returned.
	if request.method == 'GET' and request.headers['Referer'] == mainPage+url_for('query'):
		return render_template('queryAggregate.html', title = webTitle, error = "")	
	else:
		return render_template('queryAggregate.html', title = webTitle, error = "There is an issue with the query.")	

def predTypeAssignment():		#Stores the selected predefined values into a list and returns it
	#Declarations
	predType = None
	startYear = None
	industry = None
	tool = None
	objective = None
	unAuth = None
	toolList = []
	industryList = []
	objectivesList = []
	unAuthList = []
	
	#Assignment of values that have been selected by the user
	predType = request.form["predType"]
	update_predType(predType)	#Update the global predType value
	startYear = request.form["startYear"]
	toolList = request.form.getlist("tools")
	industryList = request.form.getlist("industries")
	objectivesList = request.form.getlist("objectives")
	unAuthList = request.form.getlist("unAuths")
	if "tool" in request.form:
		tool = request.form["tool"]
	if "industry" in request.form:
		industry = request.form["industry"]
	if "objective" in request.form:
		objective = request.form["objective"]
	if "unAuth" in request.form:
		unAuth = request.form["unAuth"]
	predList = [predType,startYear,industry,industryList,tool,toolList,objective,objectivesList,unAuth,unAuthList]
	return predList

@app.route('/mongo/query/result', methods = ['POST'])	#Returns the result page
def queryResults():
	querybox = None
	column2 = None
	queryType2 = None
	searchTerm2 = None
	if request.method == 'POST':
		if operation == "PreD":
			predList = predTypeAssignment()				#Get the list of predefined values
		
		elif "querybox" in request.form:
			querybox = request.form["querybox"]			#Get the user input as a string from the query box
		
		else:
			if "column" in request.form:
				column = request.form["column"]			#Get the column value
			if "queryType" in request.form:
				queryType = request.form["queryType"]	#Get the query type value
			if "searchTerm" in request.form:
				searchTerm = request.form["searchTerm"]	#Get the search term value
			#If AND values are entered, get the values
			if "column2" in request.form and "queryType2" in request.form and "searchTerm2" in request.form:
				if request.form["column2"] != "" and request.form["queryType2"] != "" and request.form["searchTerm2"] != "":
					column2 = request.form["column2"]
					queryType2 = request.form["queryType2"]
					searchTerm2 = request.form["searchTerm2"]
		
		if operation == "Aggregate":					#Do the aggregate query
			queryResult,jsonList = qm.aggregateQuery(dbCollection,querybox)
		elif operation == "PreD":						#Do the predefined query
			queryResult,jsonList = pm.doPreDQuery(dbCollection,predList)
		else:
			if querybox != None:
				queryResult,jsonList = qm.findTypedQuery(dbCollection,querybox)	#Do the typed find query
			elif column2 != None:												#Do the AND find query
				queryResult,jsonList = qm.findAndQuery(dbCollection,column,queryType,searchTerm,column2,queryType2,searchTerm2)
			else:																#Do the find query
				queryResult,jsonList = qm.findQuery(dbCollection,column,queryType,searchTerm)
		
		if queryResult and len(jsonList) >= 1:
			update_json(jsonList) 						#Update the global jsonStr value
			if len(jsonList) > limit:					#Check if the length of the list exceeds the limit
				resultLength = limit					#Set the length to the limit
				displayResults = "There are %d results but the first %d are displayed." % (len(jsonList),limit)
			else:
				resultLength = len(jsonList)			#Set the length to the length of the list
				displayResults = "There are %d results." % resultLength

			return render_template('queryResult.html', title = webTitle, len1 = resultLength, resultList = json.loads(jsonStr), displayResults = displayResults)			#Display results
		else:
			return redirect(request.referrer, code = 302)	#Returns the user to the previous page if the query fails
	
@app.route('/mongo/logout', methods = ['GET'])	#If the user presses the logout button, the connection object is destroyed
def logout():
	if db:
		update_connection(None,None)
		return redirect('/index')

@app.route('/mongo/connect', methods = ['GET'])	#Returns the connection menu
def connect():
	if db:
		return redirect('/mongo')				#If the user is already connected, redirect the user to the operation selection page
	else:
		return render_template('connect.html', title = webTitle) #Returns the connection menu

@app.route('/mongo/connect/select', methods = ['GET','POST'])	#Processes the connection type selected by the user
def connectSelect():
	if request.method == "POST":
		connectionType = request.form["connectionType"]				#Gets the connectionType 
		if connectionType != None:
			if connectionType == "Local":
				return local(connectionType)
			elif connectionType == "Atlas":
				return enterAtlas()
			elif connectionType == "Online":
				return enterOnline()
	return redirect('/mongo')

def local(connectionType):
	db = cm.doLocalConnection()										#Connects to the local instance of mongoDB
	if db != None:
		update_connection(connectionType,db)						#Updates the connection object
		return redirect('/mongo')
	else:
		return render_template('failure.html', title = webTitle)	#Returns the failure page if the connection failed
	
@app.route('/mongo/connect/atlas', methods = ['POST'])
def enterAtlas():
	return render_template('enterAtlas.html', title = webTitle) 	#Returns the Atlas connection page

@app.route('/mongo/connect/online', methods = ['POST'])
def enterOnline():
	return render_template('enterOnline.html', title = webTitle) 	#Returns the Online connection page

@app.route('/mongo/connect/validateAtlas', methods = ['POST'])
def validateA():
	if request.method == "POST":
		db = cm.doAtlasConnection(request.form["hostingServer"],request.form["clusterID"],request.form["userID"],request.form["password"])	#Calls the atlas connection function
		update_connection("Atlas",db)	#Updates the connection object
		if db != None:
			return redirect('/mongo')	#Redirects to the mongo operation selection page
		else:
			return redirect('/mongo/connect/atlas')		#Redirects the user to the same page if the connection failed
			#return render_template('failure.html', title = webTitle)

@app.route('/mongo/connect/validateOnline', methods = ['POST'])
def validateO():
	if request.method == "POST":
		if request.form["fullIP"] != None:
			db = cm.doOnlineConnectionIP(request.form["fullIP"])
		else:
			db = cm.doOnlineConnection(request.form["serverIP"],request.form["portNum"],request.form["dbName"],request.form["userID"],request.form["password"])
		update_connection("Online",db)	#Updates the connection object
		if db != None:
			return redirect('/mongo')	#Redirects to the mongo operation selection page
		else:
			return redirect('/mongo/connect/online')	#Redirects the user to the same page if the connection failed
			#return render_template('failure.html', title = webTitle)

@app.route('/mongo/store', methods = ['GET'])			#Shows the store to mongoDB page
def store():
	curCoLList = sm.getCollectionNames(db) 				#Get the list of collections in mongoDB
	return render_template('store.html', title = webTitle, len = len(curCoLList), colList = curCoLList)

@app.route('/mongo/stored', methods = ['POST'])			#Stores the JSON files
def stored():
	if request.method == "POST":
		isStored = sm.doStore(db)						#Calls the store function
		jsonList = sm.getJSONstored()					#Get the stored JSONFiles
		if isStored:
			curCoLList = sm.getCollectionNames(db)		#Get the list of collections in mongoDB
			return render_template('stored.html', title = webTitle, len = len(jsonList), sl = jsonList, isS = "The following json file(s) have been stored as the following collections.", colList = curCoLList)
		else:
			return render_template('failure.html', title = webTitle)	#Return failure page if the store function has failed

@app.route('/mongo/drop', methods = ['GET'])			#Shows the drop from mongoDB page
def drop():
	curCoLList = dm.getCollectionNames(db) 				#Get the list of collections in mongoDB
	return render_template('drop.html', title = webTitle, len = len(curCoLList), colList = curCoLList)

@app.route('/mongo/dropped', methods = ['POST'])		#Drops the collections in mongoDB
def dropped():
	if request.method == "POST":
		toDropList = request.form.getlist("drop")		#Get the list of collections to drop
		isDropped = dm.doDrop(db,toDropList)			#Calls the drop function
		if isDropped:
			return render_template('dropped.html', title = webTitle, len = len(toDropList), dl = toDropList, isD = "The following collection(s) have been dropped.")
		else:
			return render_template('failure.html', title = webTitle)	#Return failure page if the drop function has failed

@app.route('/visualisation', methods = ['GET'])
def visualisation():
	return render_template('visualisation.html', title = webTitle)		#Returns the visualisation page

@app.route('/visualisation/singularGraph', methods = ['GET','POST'])	#Retuns a graph based on the x and y axis specified
def singularGraph():
	isComplete = False
	singleParamList = exampleSingleParamList							#Assignment of the example parameter list
	
	if request.method == 'POST':
		#Gets various graph parameters
		inputFile = request.form["inputFile"]							#Gets the file uploaded by the user
		inputFileName = request.form["inputFileName"]					
		graphType = request.form["graphType"]
		graphTitle = request.form["graphTitle"]
		xAxis = request.form["xAxis"]
		yAxis = request.form["yAxis"]
		xLabel = request.form["xLabel"]
		yLabel = request.form["yLabel"]
		yLowerL = request.form["yLowerL"]
		yUpperL = request.form["yUpperL"]
		singleParamList = [graphTitle,xAxis,yAxis,xLabel,yLabel,yLowerL,yUpperL]	#Updates the singleParamList
		if inputFile:
			isComplete = vs.doGraph(graphType,singleParamList,inputFile)			#Plots graph
			update_json(inputFile)													#Updates file object
		else:
			isComplete = vs.doGraph(graphType,singleParamList,jsonStr)				#Plots graph
			inputFileName = "loaded data"
		if isComplete:
			return render_template('singularGraph.html', title = webTitle, image1 = il.graphImage, displayFile = "This is the graph generated from " + inputFileName + ".", singleParamList = singleParamList)	#Display graph
		else:
			return redirect(request.referrer, code = 302)		#Returns the user to the same page
	
	if request.method == 'GET':			#Shows the graphing page before plotting the graph
		if jsonStr:		#If there is a JSON object loaded
			return render_template('singularGraph.html', title = webTitle, loaded = jsonLoaded, singleParamList = singleParamList)
		else:
			return render_template('singularGraph.html', title = webTitle, singleParamList = singleParamList)

@app.route('/visualisation/multipleGraph', methods = ['GET','POST'])
def multipleGraph():
	isComplete = False
	multiParamList = exampleMultiParamList							#Assignment of the example parameter list
	
	if request.method == 'POST':
		graphType = "mulLine"
		#Gets various graph parameters
		inputFile = request.form["inputFile"]
		inputFileName = request.form["inputFileName"]
		graphTitle = request.form["graphTitle"]
		xLabel = request.form["xLabel"]
		yLabel = request.form["yLabel"]
		xLowerL = request.form["xLowerL"]
		xUpperL = request.form["xUpperL"]
		yLowerL = request.form["yLowerL"]
		yUpperL = request.form["yUpperL"]
		caLimit = request.form["caLimit"]
		multiParamList = [graphTitle,xLabel,yLabel,xLowerL,xUpperL,yLowerL,yUpperL,caLimit] 	#Updates the multiParamList
		if inputFile:
			isComplete = vs.doGraph(graphType,multiParamList,inputFile,predType,predTypeList) 	#Plots graph
			update_json(inputFile)																#Updates file object
		else:
			isComplete = vs.doGraph(graphType,multiParamList,jsonStr,predType,predTypeList) 	#Plots graph
			inputFileName = "loaded data"
		if isComplete:
			return render_template('multipleGraph.html', title = webTitle, image1 = il.graphImage, displayFile = "This is the graph generated from " + inputFileName + ".", multiParamList = multiParamList) #Display graph
		else:
			return redirect(request.referrer, code = 302)		#Returns the user to the same page
		
	if request.method == 'GET':
		if jsonStr:
			return render_template('multipleGraph.html', title = webTitle, loaded = jsonLoaded, multiParamList = multiParamList)
		else:
			return render_template('multipleGraph.html', title = webTitle, multiParamList = multiParamList)

@app.route('/visualisation/clustering', methods = ['POST'])
def clustering():
	if request.method == 'POST':
		if request.form["numOfClusters"] != 0 or request.form["numOfClusters"] != None:
			numOfClusters = request.form["numOfClusters"]					#Get number of clusters
		doClus = True
		hFileInput = request.form["hFileInput"]								#Get hidden file input
		cl.doClustering(int(numOfClusters),doClus,hFileInput)				#Do clustering based on file input
		return render_template('clustering.html', title = webTitle, image1 = il.elbowImage, image2 = il.clusteringImage)
	#return render_template('clustering.html', title = webTitle)

@app.route('/visualisation/clustering/elbow', methods = ['GET', 'POST'])
def elbow():
	if request.method == 'POST':
		doClus = False
		inputFile = request.form["inputFile"]								#Get file input	
		update_json(inputFile)	
		if inputFile:
			cl.doClustering(1,doClus,inputFile)								#Do clustering based on file input
			return render_template('elbow.html', title = webTitle, image1 = il.elbowImage, hfi = inputFile)
		else:
			cl.doClustering(1,doClus,jsonStr)								#Do clustering based on JSON string
			return render_template('elbow.html', title = webTitle, image1 = il.elbowImage, hfi = jsonStr)
		
	if request.method == 'GET':
		if jsonStr:
			return render_template('elbow.html', title = webTitle, loaded = jsonLoaded)
		else:
			return render_template('elbow.html', title = webTitle)

@app.route('/visualisation/regression', methods = ['GET', 'POST'])
def regression():
	if request.method == 'POST':
		termList = []
		valueList = []
		inputFileName = request.form["inputFileName"]						#Get file name
		inputFile = request.form["inputFile"]								#Get file input
		update_json(inputFile)	
		if inputFile:
			termList,valueList = reg.doRegression(inputFile)				#Do regression based on file input
		else:
			termList,valueList = reg.doRegression(jsonStr)					#Do regression based on JSON string
		return render_template('regression.html', title = webTitle, image1 = il.regressionImage, len = len(termList), tl = termList, vl = valueList, displayFile = "This is the graph generated from " + inputFileName )
	
	if request.method == 'GET':
		if jsonStr:
			return render_template('regression.html', title = webTitle,len = 0, loaded = jsonLoaded)
		else:			
			return render_template('regression.html', title = webTitle,len = 0)
			
if __name__ == "__main__":						#Flask main function
	app.run(debug=True)							#Debug is enabled to catch exceptions
	port = int(os.environ.get('PORT', 5000))	#Port is specified
	app.run(host=hostURL, port=port)