import dateutil.parser
import re
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.prdbReplacement as pr

# Declarations
nullValue = mp.nullValue
prdbType = mp.prdbType
No = "No"
date = "date"
victim = "victim"
org_type = "Type of organization"
location = "location"
variety = "variety"
records_affected = "records_affected"
description = "Description of incident"
info_source = "info_source"
source_link = "source_link"
country = "country"
US = "US"
paper = "paper"
date = "date"
day = "day"
month = "month"
year = "year"
isEstimate = "isEstimate"

# Referencing the lists dictionaries in the prdbReplacement file
vectorList = pr.vectorList
varietyDict = pr.varietyDict
varietyList = pr.varietyList		
toolReplacementDict = pr.toolReplacementDict
vulnerabilityReplacementDict = pr.vulnerabilityReplacementDict
actionReplacementDict = pr.actionReplacementDict		
TVARemoveList = pr.TVARemoveList
industryReplacementDict = pr.industryReplacementDict

# Function can be uncommented and used to remove data breach incidents involving the mishandling of paper documents
# def checkDescriptionPaper(JSONDict):														
	# if description in JSONDict:
		# if re.search(paper,JSONDict[description],re.IGNORECASE): 														
				# return False
		# else:
			# return True

# Clean lists to remove unknown other and na
def parseList(elist):																
	if isinstance(elist,list): 					
		elist = list(dict.fromkeys(elist))		#Remove duplicates
		while nullValue in elist:				#Remove null values
			elist.remove(nullValue)
		if len(elist) >= 1:
			return elist
		else:
			return nullValue
	else:
		return nullValue	

def addEntryDate(JSONDict):															
	if "Date Made Public" in JSONDict:		
		dt = dateutil.parser.parse(JSONDict["Date Made Public"])															#Dates have to be parsed to ISO date
		return 	{date : dt, year : dt.year, month : dt.month, day : dt.day, isEstimate : No}

# The company field contains the victim
def addVictim(JSONDict):
	vList = []
	if "Company" in JSONDict:
		vList.append(JSONDict["Company"])
		if len(vList) >= 1:
			return vList
		else:
			return nullValue

# The industry values have to be normalized		
def addIndustry(JSONDict):
	industryList = []
	if org_type in JSONDict:
		if JSONDict[org_type] != "UNKN":
			industryList.append(JSONDict[org_type])
			for indus in industryReplacementDict:
				if industryList[0] == indus:
					industryList.pop()
					industryList.append(industryReplacementDict[indus])
	if len(industryList) >= 1:
		return industryList
	else:
		return nullValue

# Most prdb incidents are based in US except the listed incidents with states		
def addCountry(JSONDict):												
	if "State" in JSONDict:
		if JSONDict["State"] == "Beijing":
			return "CN"
		if JSONDict["State"] == "Dublin":
			return "IE"
		if JSONDict["State"] == "British Columbia":
			return "CA"
		if JSONDict["City"] == "Hong Kong":
			return "HK"
		if JSONDict["City"] == "Hamburg":
			return "DE"
	return US

# If the incident has a city or state, it should be merged into one field
def addState(JSONDict):
	if "City" and "State" in JSONDict:
		if JSONDict["City"] != "" and JSONDict["State"] != "":
			return JSONDict["City"] + ", " + JSONDict["State"]
		else:
			if JSONDict["State"] != "":
				return JSONDict["State"]
			if JSONDict["City"] != "":
				return JSONDict["State"]
			else:
				return nullValue

# The vector can be retrieved from the description by doing a substring search
def getVector(JSONDict):
	vectors = []
	if description in JSONDict:
		for substr in vectorList:
			if re.search(substr,JSONDict[description],re.IGNORECASE): 
				vectors.append(substr)
	return vectors

# The field type of breach contains a short form of the type of attack and it must be translated/normalized from the short form to the long form		
def getVariety(JSONDict):																				
	varietys = []
	if "Type of breach" in JSONDict:
		for vary in varietyDict:
			if JSONDict["Type of breach"] == vary :
				varietys.append(varietyDict[vary])
	if description in JSONDict:
		for substr in varietyList:
			if re.search(substr,JSONDict[description],re.IGNORECASE): 
				varietys.append(substr)
	return varietys 

# The variety and vector lists are combined into a single list and parsing occurs to retrieve the corressponding tools, vulnerabilities and actions from the list. Three lists are returned 
def addTVA(JSONDict):		#attribute.integrity.variety
	fullList = []
	fullList.extend(getVariety(JSONDict))
	fullList.extend(getVector(JSONDict))
	return parseList(parseToolList(fullList)),parseList(parseVulnerabilityList(fullList)),parseList(parseActionList(fullList))

# Obtaining the tools from the list
def parseToolList(fullList):
	toolList = []
	for tool,toReplaceList in toolReplacementDict.items():
		for term in toReplaceList:
			for t in fullList:
				if t == term: 
					toolList.append(tool)
					toolList.append(term)	
	for elem in TVARemoveList:
		while elem in toolList:
			toolList.remove(elem)
	return toolList

# Obtaining the vulnerabilities from the list
def parseVulnerabilityList(fullList):
	vulnerabilityList = []
	for vulnerability,toReplaceList in vulnerabilityReplacementDict.items():
		for term in toReplaceList:
			for vuln in fullList:
				if vuln == term: 
					vulnerabilityList.append(vulnerability)
					vulnerabilityList.append(term)	
	for elem in TVARemoveList:
		while elem in vulnerabilityList:
			vulnerabilityList.remove(elem)
	return vulnerabilityList

# Obtaining the actions from the list	
def parseActionList(fullList):
	actionList = []
	for action,toReplaceList in actionReplacementDict.items():
		for term in toReplaceList:
			for act in fullList:
				if act == term: 
					actionList.append(action)
					actionList.append(term)	
	for elem in TVARemoveList:
		while elem in actionList:
			actionList.remove(elem)
	return actionList	
				
def addRecordsAffected(JSONDict):
	if "Total Records" in JSONDict:
		return JSONDict["Total Records"]
		
def addTarget(JSONDict):
	ra = addRecordsAffected(JSONDict)
	return {"targeted" : nullValue, "records_affected" : ra, "assets_affected" : nullValue}
		
def addDescription(JSONDict):
	if description in JSONDict:
		return JSONDict[description]

def addInfoSource(JSONDict):
	if info_source in JSONDict:
		return JSONDict[info_source]
		
def addSourceLink(JSONDict):
	if "Source URL" in JSONDict and JSONDict["Source URL"] != "":
		return JSONDict["Source URL"]

def addValues(JSONDict,parseDict):
	#parseDict["type"] = prdb																				#Always type 
	parseDict["industry"] = addIndustry(JSONDict)															#industry
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	if parseDict["industry"] != None:																		# If the industry is null, the incident should not be included in the database 
		parseDict["entry_date"] = addEntryDate(JSONDict)													#Date
	else:
		parseDict["entry_date"] = nullValue
	parseDict["victim"] = addVictim(JSONDict)																#victim
	parseDict["country"] = addCountry(JSONDict)																#country
	parseDict["state"] = addState(JSONDict)																	#state
	parseDict["tool"],parseDict["vulnerability"],parseDict["action"] = addTVA(JSONDict)						#Tool Vulnerability and Action
	parseDict["target"] = addTarget(JSONDict)																#Records Affected
	parseDict["description"] = addDescription(JSONDict)														#Description
	parseDict["info_source"] = addInfoSource(JSONDict)														#Info Source
	parseDict["source_link"] = addSourceLink(JSONDict)														#Source Link
	return parseDict