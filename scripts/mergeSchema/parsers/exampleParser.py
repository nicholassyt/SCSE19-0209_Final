from datetime import datetime
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.exampleReplacement as er

# This file is just an example of the way a parser should be created
# The schema file can be referenced to discover the fields
# The fields in the functions should be retrieved based on the field names in the original JSON file

# Declarations of common terms used
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

# Replacement dictionaries are used when the values need to be normalized
industryReplacementDict = er.industryReplacementDict

# Dates should be stored as follows
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

# Industries should be normalized
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

# The target field is a dictionary
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
	#parseDict["type"] = type 																							

	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)											
	parseDict["victim"] = addVictim(JSONDict)													
	parseDict["industry"] = addIndustry(JSONDict)	
	parseDict["country"] = nullValue														
	parseDict["state"] = nullValue																
	parseDict["target"] = addTarget(JSONDict)
	parseDict["description"] = nullValue													
	parseDict["info_source"] = addInfoSource(JSONDict)													
	parseDict["source_link"] = addSourceLink(JSONDict)
	
	# Fields may not be present in all data sources
	parseDict["employee_count"] = nullValue	
	parseDict["attacker"] = nullValue			#attacker name, origin and role
	parseDict["objectives"] = nullValue															
	parseDict["discovered_by"] = nullValue
	parseDict["cve"] = nullValue																		
	parseDict["malware_used"] = nullValue																
	parseDict["tool"] = nullValue	
	parseDict["vulnerability"] = nullValue	
	parseDict["action"] = nullValue	
	parseDict["unauthorized_result"] = nullValue	
	parseDict["monetary_loss"] = nullValue    
	return parseDict