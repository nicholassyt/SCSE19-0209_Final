from datetime import datetime
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.wikiReplacement as wr

# Declarations
victim = "victim"
source_link = "source_link"
industry = "industry"
date_year = "date_year"
records_affected = "records_affected"
info_source = "info_source"
year = "year"
month = "month"
day = "day"
type = "type"
No = "No"
date = "date"
isEstimate = "isEstimate"
nullValue = mp.nullValue

# Referencing the dictionaries in the wikiReplacement file
industryReplacementDict = wr.industryReplacementDict

# The wiki data source only provides the year. The dates are parsed to create a proper datetime.
def addEntryDate(JSONDict):#JSONDict[date_year]
	if date_year in JSONDict and JSONDict[date_year] != "":
		if JSONDict[date_year] != nullValue:
			if isinstance(JSONDict[date_year],str):
				eyear = int(JSONDict[date_year].split('-')[0])
			else:
				eyear = JSONDict[date_year]
			emonth = 1
			eday = 1
			dt = datetime(eyear,emonth,eday)		#Dates have to be parsed to ISO date
			return 	{date : dt, year : eyear, month : emonth, day : eday, isEstimate : No}

# The industries have to be normalized
def addIndustry(JSONDict):
	if industry in JSONDict and JSONDict[industry] != "":
		for ind,toReplaceList in industryReplacementDict.items():
			for term in toReplaceList:
				if JSONDict[industry] == term:
					return list(ind)
	else:
		return nullValue

def addVictim(JSONDict):
    if victim in JSONDict:
        return JSONDict[victim]

def addRecordsAffected(JSONDict):
	if records_affected in JSONDict:
		if JSONDict[records_affected] != "" and JSONDict[records_affected] != " " and JSONDict[records_affected] != nullValue:
			recA = JSONDict[records_affected].replace(',','')
			if recA.isdigit():
				return int(recA)
			else:
				return nullValue
		else:
			return nullValue

def addTarget(JSONDict):
	ra = addRecordsAffected(JSONDict)
	return {"targeted" : nullValue, "records_affected" : ra, "assets_affected" : nullValue}

def addInfoSource(JSONDict):
	if info_source in JSONDict:
		if JSONDict[info_source] != "":
			return JSONDict[info_source]
		else:
			return nullValue
		
def addSourceLink(JSONDict):
	if source_link in JSONDict:
		return JSONDict[source_link]

def addValues(JSONDict, parseDict):
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)													#Date
	parseDict["victim"] = addVictim(JSONDict)																#victim
	parseDict["industry"] = addIndustry(JSONDict)																#industry
	parseDict["country"] = nullValue														#country
	parseDict["state"] = nullValue																#state
	#parseDict["tool"],parseDict["vulnerability"],parseDict["action"] = nullValue							#Tool Vulnerability and Action
	parseDict["target"] = addTarget(JSONDict)
	parseDict["description"] = nullValue													#Description
	parseDict["info_source"] = addInfoSource(JSONDict)														#Info Source
	parseDict["source_link"] = addSourceLink(JSONDict)														#Source Link
	return parseDict

