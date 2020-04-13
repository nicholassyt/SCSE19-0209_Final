from datetime import datetime
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.healthReplacement as hr

# Declarations
state = "state"
victim = "victim"
country = "country"
description = "description"
location = "location"
info_source = "info_source"
records_affected = "records_affected"
industry = "industry"
year = "year"
month = "month"
day = "day"
type = "type"
No = "No"
date = "date"
isEstimate = "isEstimate"

# Referencing the dictionaries in the healthReplacement file
unAuthResultReplacementDict = hr.unAuthResultReplacementDict
industryReplacementDict = hr.industryReplacementDict
actionReplacementDict = hr.actionReplacementDict
countryReplacementDict = hr.countryReplacementDict
nullValue = mp.nullValue

def addEntryDate(JSONDict):															
	if year in JSONDict and JSONDict[year] != "":
		if JSONDict[year] != nullValue:
			eyear = JSONDict[year]
			emonth = JSONDict[month]
			eday = JSONDict[day]
			dt = datetime(eyear,emonth,eday)		#Dates have to be parsed to ISO date
			return 	{date : dt, year : eyear, month : emonth, day : eday, isEstimate : No}

# The victim field is a list as there may be more than one victim
def addVictim(JSONDict):
	vList = []
	if victim in JSONDict:
		vList.append(JSONDict[victim])
		if len(vList) >= 1:
			return vList
		else:
			return nullValue

# The industry field has to be normalized by referencing the industryReplacementDict
def addIndustry(JSONDict):
	if industry in JSONDict:
		for ind,toReplaceList in industryReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[industry] == term:
					return list(ind)	

# The country string has to be converted to the two country code
def addCountry(JSONDict):
	if country in JSONDict:
		if JSONDict[country] != "":
			for countryCode,countryStr in countryReplacementDict.items():
				if JSONDict[country] == countryStr:
					return countryCode
			return JSONDict[country]
		else:
			return nullValue

def addState(JSONDict):
	if state in JSONDict:
		if JSONDict[state] != "":
			return JSONDict[state]
		else:
			return nullValue

def addTarget(JSONDict):
	ra = addRecordsAffected(JSONDict)
	if ra != nullValue:
		return {"targeted" : nullValue, "records_affected" : ra, "assets_affected" : nullValue}
	else:
		return nullValue
	
def addRecordsAffected(JSONDict):
	if records_affected in JSONDict:
		if JSONDict[records_affected] != "\"\"":
			return JSONDict[records_affected]
		else:
			return nullValue
			
def addDescription(JSONDict):
	if description in JSONDict:
		if JSONDict[description] != "":
			return JSONDict[description]
		else:
			return nullValue

# The actions have to be normalized
def addAction(JSONDict):
	actionList = []
	if type in JSONDict:
		for action,toReplaceList in actionReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[type] == term:
					actionList.append(action)
					actionList.append(JSONDict[type])
					return actionList			

# The unauthorized results have to be normalized
def addUnAuthResult(JSONDict):
	unAuthList = []
	if type in JSONDict:
		for unAuth,toReplaceList in unAuthResultReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[type] == term:
					unAuthList.append(unAuth)
					return unAuthList			

def addValues(JSONDict, parseDict):
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)									#Date
	parseDict["victim"] = addVictim(JSONDict)											#victim
	parseDict["industry"] = addIndustry(JSONDict)										#industry
	parseDict["country"] = addCountry(JSONDict)											#country
	parseDict["state"] = addState(JSONDict)												#state
	#parseDict["tool"],parseDict["vulnerability"] = nullValue							#Tool Vulnerability and Action
	parseDict["action"] = addAction(JSONDict)
	parseDict["unauthorized_result"] = addUnAuthResult(JSONDict)
	parseDict["target"] = addTarget(JSONDict)											#Records Affected
	parseDict["description"] = addDescription(JSONDict)									#Description
	parseDict["info_source"] = nullValue												#Info Source
	parseDict["source_link"] = nullValue												#Source Link
	return parseDict