import json
import csv
import os
import re
from datetime import datetime
from currency_converter import CurrencyConverter
from dateutil.relativedelta import relativedelta
import dateutil.parser
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.vcdbReplacement as vr

#Load values from parameters file
naicsJSONFile = os.path.join(os.path.dirname(__file__), "naics.json")
fieldsToAdd = mp.fieldsToAdd
nullValue = mp.nullValue

#Declarations
unknown = "unknown"
Unknown = "Unknown"
other = "Other"
NA = "NA"
Yes = "Yes"
No = "No"

vcdbType = mp.vcdbType
impact = "impact"
victim  = "victim"
victim_id = "victim_id"
industry = "industry"
country = "country"
countryUS = "US"
state = "state"
employee_count = "employee_count"

timeline = "timeline"
incident = "incident"
day = "day"
month = "month"
year = "year"

# Currency converter for conversion from other currencies to USD
cc = CurrencyConverter()
monetaryLossThreshold = 100000000000
iso_currency_code = "iso_currency_code"
currencyUSD = "USD"
overall_amount = "overall_amount"
overall_max_amount = "overall_max_amount"
amount = "amount"
loss = "loss"

timeline = "timeline"
incident = "incident"
date = "date"
day = "day"
month = "month"
year = "year"
isEstimate = "isEstimate"

plus = "plus"
notification = "notification"
created = "created"

targeted = "targeted"
actor = "actor"
name = "name"
partner = "partner"
external = "external"
internal = "internal"
variety = "variety"
motive = "motive"

cve = "cve"
malware = "malware"
action = "action"
hacking = "hacking"
social = "social"
physical = "physical"
vector = "vector"
error = "error"
misuse = "misuse"
result = "result"

attribute = "attribute"
availability = "availability"
duration = "duration"
unit = "unit"
value = "value"

confidentiality = "confidentiality"
data_total = "data_total"
data_victim = "data_victim"
data = "data"
integrity = "integrity"
data_disclosure = "data_disclosure"

asset = "asset" 
assets = "assets"
management = "management" 
ownership = "ownership"
total_amount = "total_amount"

compromise = "compromise"
exfiltration = "exfiltration"
discovery = "discovery"
containment = "containment"

control_failure = "control_failure"
summary = "summary"
analyst = "analyst"
investigator = "investigator" 
reference = "reference"
discovery_method = "discovery_method"
hardwareTampering = "Hardware tampering"
softwareInstallation = "Software installation"	

# Regex
defacedRegex = "defaced?"
spyRegex = "sp(y|ies)"

# Certain fields may contain the values that are required. The list can be iterated to match the fields in the vcdb json file. 
fieldsList = [error,hacking,malware,misuse,physical,social]

# Removal of null or unknown values from a list
removalList = [unknown,Unknown,other,NA,nullValue]

# For parsing of the resolution date
unitDict = {None : 0, 'Never' : 0, 'Unknown' : 0,  'NA' : 0, 'Seconds' : 1,'Minutes' : 2, 'Hours' : 3, 'Days' : 4, 'Weeks': 5, 'Months' : 6, 'Years' : 7}

# Referencing the lists and dictionaries in the vcdbReplacement file
industryReplacementDict = vr.industryReplacementDict
attackerRoleReplacementDict = vr.attackerRoleReplacementDict
attackerRoleRemoveList = vr.attackerRoleRemoveList
objectivesReplacementDict = vr.objectivesReplacementDict
objectivesRemoveList = vr.objectivesRemoveList
vectorReplacementDict = vr.vectorReplacementDict
vectorRemoveList = vr.vectorRemoveList
varietyRemoveList = vr.varietyRemoveList
toolReplacementDict = vr.toolReplacementDict
vulnerabilityReplacementDict = vr.vulnerabilityReplacementDict
actionReplacementDict = vr.actionReplacementDict
TVARemoveList = vr.TVARemoveList
unAuthResultReplacementDict = vr.unAuthResultReplacementDict
unAuthResultRemoveList = vr.unAuthResultRemoveList
targetReplacementDict = vr.targetReplacementDict
targetRemoveList = vr.targetRemoveList
malwareReplacementDict = vr.malwareReplacementDict

def populateIndustryData():														#Loads data from naics.json
	with open(naicsJSONFile, encoding='utf-8') as data:							#File must be opened with utf-8 encoding as there are symbols errors without it
			json_data = json.load(data)											#Call json.load to load json data. 
			data.close()
			return json_data
# industryData is used to convert industries from their NAICS codes
industryData = populateIndustryData()
		
def parseList(elist):																#Clean lists to remove unknown other and na
	if isinstance(elist,list): 
		elist = list(dict.fromkeys(elist))											#Remove duplicates
		for elem in removalList:
			while elem in elist:
				elist.remove(elem)
		if len(elist) >= 1:
			return elist
		else:
			return nullValue
	else:
		return nullValue															#Return null if list is empty

def addIncidentDate(JSONDict):														#timeline.incident.day,timeline.incident.month,timeline.incident.year are integers						
	yearint = nullValue
	monthint = nullValue
	dayint = nullValue
	dt = nullValue
	estimate = Yes
	if timeline in JSONDict:#Obtaining the incident date
		if incident in JSONDict[timeline]:
			if day in JSONDict[timeline][incident]:
				dayint = JSONDict[timeline][incident][day]
			if month in JSONDict[timeline][incident]:
				monthint = JSONDict[timeline][incident][month]
			if year in JSONDict[timeline][incident]:
				yearint = JSONDict[timeline][incident][year]
		if yearint != nullValue and monthint != nullValue and dayint != nullValue:#If the year, month and day are not null it is not an estimate
			estimate = No
			dayint,monthint,estimate = checkDayMonth(dayint,monthint)
			dt = datetime(yearint,monthint,dayint).isoformat()
		elif yearint != nullValue and monthint != nullValue:#If the year, month and day are null it is an estimate
			dt = datetime(yearint,monthint,1).isoformat()
		elif yearint != nullValue and monthint == nullValue and dayint == nullValue:
			dt = datetime(yearint,1,1).isoformat()
		indicidentDateDict = { date : dt, year : yearint, month : monthint, day : dayint, isEstimate : estimate}
		return indicidentDateDict

def addResolutionDate(JSONDict,indicidentDateDict):								#Resolution date is calculated by adding relevant time unit and value to the incident date. uses relativedelta
	if indicidentDateDict[isEstimate] == No:
		value,unit = getResolution(JSONDict)									#Get the resolution value and unit
		if value != nullValue and unit != nullValue:
			dt =  dateutil.parser.parse(indicidentDateDict[date])
			# Add the datetime according to the value and unit that was returned
			if unit == "Seconds":
				dt = dt + relativedelta(seconds=+value)
			elif unit == "Minutes":
				dt = dt + relativedelta(minutes=+value)
			elif unit == "Hours":
				dt = dt + relativedelta(hours=+value)
			elif unit == "Days":
				dt = dt + relativedelta(days=+value)
			elif unit == "Weeks":
				dt = dt + relativedelta(weeks=+value)	
			elif unit == "Months":	
				dt = dt + relativedelta(months=+int(value))	
			elif unit == "Years":
				dt = dt + relativedelta(years=+int(value))	
			resolutionDateDict = { date : dt, year : dt.year, month : dt.month, day : dt.day, "resolution_value" : value, "resolution_unit" : unit}
			return resolutionDateDict

def getResolution(JSONDict): 
	#timeline.compromise.unit timeline.compromise.value timeline.exfiltration.unit timeline.exfiltration.value 
	#timeline.discovery.unit timeline.discovery.value timeline.containment.unit	timeline.containment.value
	#Declare null values
	timeComUnit = nullValue
	timeComValue = nullValue
	timeExUnit = nullValue
	timeExValue = nullValue
	timeDisUnit = nullValue
	timeDisValue = nullValue
	timeConUnit = nullValue
	timeConValue = nullValue
	largestUnit = nullValue
	largestValue = nullValue
	#Retrieve values from the timeline fields and assign to variables
	if timeline in JSONDict:
		if compromise in JSONDict[timeline]:
			if unit in JSONDict[timeline][compromise]:
				timeComUnit = JSONDict[timeline][compromise][unit]
			if value in JSONDict[timeline][compromise]:
				timeComValue = JSONDict[timeline][compromise][value]
		if exfiltration in JSONDict[timeline]:
			if unit in JSONDict[timeline][exfiltration]:
				timeExUnit = JSONDict[timeline][exfiltration][unit]
			if value in JSONDict[timeline][exfiltration]:
				timeExValue = JSONDict[timeline][exfiltration][value]
		if discovery in JSONDict[timeline]:
			if unit in JSONDict[timeline][discovery]:
				timeDisUnit = JSONDict[timeline][discovery][unit]
			if value in JSONDict[timeline][discovery]:
				timeDisValue = JSONDict[timeline][discovery][value]
		if containment in JSONDict[timeline]:
			if unit in JSONDict[timeline][containment]:
				timeConUnit = JSONDict[timeline][containment][unit]
			if value in JSONDict[timeline][containment]:
				timeConValue = JSONDict[timeline][containment][value]
	#Assign the largest unit and value
		largestUnit = timeComUnit
		largestValue = timeComValue
		if unitDict[timeExUnit] > unitDict[largestUnit]:
			largestUnit = timeExUnit
			largestValue = timeExValue
		if unitDict[timeDisUnit] > unitDict[largestUnit]:
			largestUnit = timeDisUnit
			largestValue = timeDisValue
		if unitDict[timeConUnit] > unitDict[largestUnit]:
			largestUnit = timeConUnit
			largestValue = timeConValue
		if largestValue != nullValue and largestUnit != nullValue:
			return largestValue,largestUnit								#Return the largest unit and value
		else:
			return nullValue,nullValue
	else:
		return nullValue,nullValue
	
def addNotificationDate(JSONDict):										#plus.timeline.notification.day plus.timeline.notification.month plus.timeline.notification.year are integers
	yearint = nullValue
	monthint = nullValue
	dayint = nullValue
	dt = nullValue
	estimate = Yes
	if plus in JSONDict:#Obtaining the notification date
		if timeline in JSONDict[plus]:
			if day in JSONDict[plus][timeline][notification]:
				dayint = JSONDict[plus][timeline][notification][day]				
			if month in JSONDict[plus][timeline][notification]:
				monthint = JSONDict[plus][timeline][notification][month]				
			if year in JSONDict[plus][timeline][notification]:
				yearint = JSONDict[plus][timeline][notification][year]	
		if yearint != nullValue and monthint != nullValue and dayint != nullValue:#If the year, month and day are not null it is not an estimate
			estimate = No
			dayint,monthint,estimate = checkDayMonth(dayint,monthint)
			dt = datetime(yearint,monthint,dayint).isoformat()
		elif yearint != nullValue and monthint != nullValue:
			if monthint > 12:
				monthint = 1
			dt = datetime(yearint,monthint,1).isoformat()
		elif yearint != nullValue and monthint == nullValue and dayint == nullValue:
			dt = datetime(yearint,1,1).isoformat()
		if yearint == 13: # error within the database
			yearint = 2017
			dayint = 13
		notificationDateDict = { date : dt, year : yearint, month : monthint, day : dayint, isEstimate : estimate}

		return notificationDateDict	
	
def addEntryDate(JSONDict):	# The entry date should always be present
	if plus in JSONDict:
		if created in JSONDict[plus]:
			dtstring = JSONDict[plus][created]
			dt = dateutil.parser.parse(dtstring)
			entryDateDict = { date : dt, year : dt.year, month : dt.month, day : dt.day}
			return entryDateDict

def checkDayMonth(dayint,monthint):	#Some dates have been assigned wrongly
	estimate = No
	if monthint == 2:				#Accounts for February
		if dayint > 28:
			dayint = 28
	if dayint > 31: 				#There are only 31 days in a month
		dayint = 1
		estimate = Yes
	if monthint > 12:				#There are only 12 Months
		monthint = 1
		estimate = Yes
	return dayint,monthint,estimate		

def addVictim(JSONDict):	#victim.victim_id is a str value
	vList = []
	if victim in JSONDict:
		if victim_id in JSONDict[victim]:
			vList.append(JSONDict[victim][victim_id])
			if len(vList) >= 1:
				return vList 										#Returns the victim id as a list
			else:
				return nullValue
				
def addIndustry(JSONDict): #victim.industry converted from NAICS Codes which are integer values
	if victim in JSONDict:
		if industry in JSONDict[victim]:
			industryTitle = convertIndustry(JSONDict[victim][industry])					#Do the industry conversion against the codes in naics.json 
			if industryTitle != nullValue:
				industryTitle = replaceOrgType(industryTitle)
			if industryTitle == nullValue:												#For error checking
				print(JSONDict[victim][victim_id],"-",JSONDict[victim][industry])
			return industryTitle
	
def convertIndustry(naicsCode):
	for line in industryData:
		if naicsCode == line["Code"]:														#Compare naics code against the codes in naics.json
			return line["Title"]															#Return the industry name
		elif naicsCode == "48-49" and line["Code"] == 48:									#Certain NAICS codes have a '-'
			return line["Title"]

def replaceOrgType(industryTitle):															#Parse industries against the vcdbReplacement file
	for orgType,toReplaceList in industryReplacementDict.items():
		for term in toReplaceList:
			if re.search(term,industryTitle,re.IGNORECASE): 
				return list(orgType)
	
def addCountry(JSONDict):		#victim.country is a list
	if victim in JSONDict:
		if country in JSONDict[victim]:
			if Unknown in JSONDict[victim][country]:										#nullValue will be returned if the value is Unknown
				return nullValue
			else: 
				return JSONDict[victim][country][0]											#Original value is a list. The first element in the list is the country 

def addState(JSONDict):	#victim.state is a str value
	if victim in JSONDict:
		if state in JSONDict[victim]:
			if Unknown in JSONDict[victim][state] or JSONDict[victim][state] == "":			#nullValue will be returned if the value is Unknown or empty
				return nullValue
			else:
				return JSONDict[victim][state]

def addEmpCount(JSONDict):	#victim.employee_count is a integer value
	if victim in JSONDict:
		if employee_count in JSONDict[victim]:
			if JSONDict[victim][employee_count] == Unknown:									#nullValue will be returned if the value is Unknown
				return nullValue
			else:
				return JSONDict[victim][employee_count]										
	
def getAttackerName(JSONDict):	#actor.external.name actor.partner.name are lists
	actorList = []																			#Declare list as there may be multiple actors
	if actor in JSONDict:
		if external in JSONDict[actor]:
			if name in JSONDict[actor][external]:
				actorList.extend(JSONDict[actor][external][name])							#Extend to include list into actorList
		if partner in JSONDict[actor]:
			if name in JSONDict[actor][partner]:
				actorList.extend(JSONDict[actor][partner][name])							#Extend to include list into actorList
		return parseList(actorList)
	
def getAttackerOrigin(JSONDict): #actor.external.country actor.partner.country are lists
	originList = []
	if actor in JSONDict:
		if external in JSONDict[actor]:
			if country in JSONDict[actor][external]:
				originList.extend(JSONDict[actor][external][country])					#Extend to include list into originList
		if partner in JSONDict[actor]:
			if country in JSONDict[actor][partner]:
				originList.extend(JSONDict[actor][partner][country])					#Extend to include list into originList
		return parseList(originList)

def getAttackerRole(JSONDict,records_action,desc):	#actor.external.variety actor.internal.variety are lists
	roleList = []
	roleList.append(getSpiesAndVandals(records_action,desc))
	if actor in JSONDict:
		if external in JSONDict[actor]:
			if variety in JSONDict[actor][external]:
				roleList.extend(JSONDict[actor][external][variety])							#Extend to include list into roleList
		if internal in JSONDict[actor]:
			if variety in JSONDict[actor][internal]:
				roleList.extend(JSONDict[actor][internal][variety])							#Extend to include list into roleList
		return parseList(parseAttackerRoleList(roleList))

def parseAttackerRoleList(roleList):														#Parse Attacker roles against the vcdbReplacement file
	for role,toReplaceList in attackerRoleReplacementDict.items():
		for term in toReplaceList:
			for r in roleList:
				if r == term: 
					roleList.append(role)
					break
	for elem in attackerRoleRemoveList:														# Remove attacker roles from the list
		while elem in roleList:
			roleList.remove(elem)
	return roleList		

def addAttackerToDict(JSONDict,records_action,desc):										# Form Attacker dict
	attackerDict = {"name" : getAttackerName(JSONDict), "origin" : getAttackerOrigin(JSONDict), "role" : getAttackerRole(JSONDict,records_action,desc)}
	return attackerDict

def getSpiesAndVandals(records_action,desc):												# If the action is defacement, the attacker role should be vandal
	if records_action != nullValue:
		if "Defacement" in records_action:
			return "Vandals"
	if desc != nullValue:
		if re.search(defacedRegex,desc,re.IGNORECASE): 										# If the description contains vandals, the attacker role should be vandal
			return "Vandals"
		if re.search(spyRegex,desc,re.IGNORECASE):											# If the description contains spies, the attacker role should be spies
			return "Spies"
	
def addObjectives(JSONDict):					#actor.external.motive ,actor.internal.motive actor.partner.motive are lists
	purposeList = []
	if targeted in JSONDict:
			purposeList.append(JSONDict[targeted])
	if actor in JSONDict:
		if external in JSONDict[actor]:
			if motive in JSONDict[actor][external]:
				purposeList.extend(JSONDict[actor][external][motive])					#Extend to include list into purposeList
		if internal in JSONDict[actor]:
			if motive in JSONDict[actor][internal]:
				purposeList.extend(JSONDict[actor][internal][motive])					#Extend to include list into purposeList
		if partner in JSONDict[actor]:
			if motive in JSONDict[actor][partner]:
				purposeList.extend(JSONDict[actor][partner][motive])					#Extend to include list into purposeList
	if impact in JSONDict:
		if loss in JSONDict[impact]:
			if variety in JSONDict[impact][loss][0]: 
				purposeList.append(JSONDict[impact][loss][0][variety])
	return parseList(parsePurposeList(purposeList))

def parsePurposeList(purposeList):														#Parse Purpose against the vcdbReplacement file
	for purpose,toReplaceList in objectivesReplacementDict.items():
		for term in toReplaceList:
			for pur in purposeList:
				if pur == term: 
					purposeList.append(purpose)
					break
	for elem in objectivesRemoveList:
		while elem in purposeList:
			purposeList.remove(elem)
	return purposeList		
					
def addCVE(JSONDict): 					#action.malware.cve action.hacking.cve is a str
	aCVE = nullValue
	if action in JSONDict:
		if malware in JSONDict[action]:
			if cve in JSONDict[action][malware]:
				aCVE = JSONDict[action][malware][cve]
		elif hacking in JSONDict[action]:
			if cve in JSONDict[action][hacking]:
				aCVE = JSONDict[action][hacking][cve]
		return parseCVE(aCVE)
	else:
		return nullValue

def parseCVE(aCVE):										# Parsing wrong CVE values. The CVE values may have multiple values or missing '-'
	if aCVE == nullValue or aCVE == "":
		return nullValue
	elif ',' in aCVE:
		cveList = [x.strip() for x in aCVE.split(',')]
		return cveList
	elif ';' in aCVE:
		cveList = [x.strip() for x in aCVE.split(';')]
		return cveList
	elif aCVE == 'CVE 2012-4792':
		return ['CVE-2012-4792']
	elif 'vuln' in aCVE:
		return nullValue
	elif unknown in aCVE:
		return nullValue
	elif 'Wordpress' in aCVE:
		return nullValue
	else:
		return [aCVE]
				
def addMalware(JSONDict): 				#action.malware.name is a str
	malwareList = []
	if action in JSONDict:
		if malware in JSONDict[action]:
			if name in JSONDict[action][malware]:
				if JSONDict[action][malware][name] != unknown:
					malwareList = parseMalware(JSONDict[action][malware][name])		
	if len(malwareList) >= 1 and malwareList[0] != "":
		return malwareList
	else:
		return nullValue

def parseMalware(aMalware):						# Parsing wrong malware values. There may be multiple malwares or there is a need to parse Malware against the vcdbReplacement file
	malwareList = [aMalware]
	if "," in malwareList[0]:
		malwareList = [x.strip() for x in aMalware.split(',')]
	elif ";" in malwareList[0]:
		malwareList = [x.strip() for x in aMalware.split(';')]
	
	for malw,toReplaceList in malwareReplacementDict.items():	
		for term in toReplaceList:
			i = 0
			for mal in malwareList:
				if mal == term:
					malwareList[i] = malw
				i+=1
	return malwareList
	
def getVector(JSONDict): #action.social.vector action.malware.vector action.error.vector action.hacking.vector action.physical.vector are lists
	vectorList = []
	if action in JSONDict:
		for type in fieldsList:
			if type in JSONDict[action]:
				if vector in JSONDict[action][type]:
					vectorList.extend(JSONDict[action][type][vector])					#Extend to include list into vectorList
		return parseVectorList(vectorList)									

def parseVectorList(vectorList):
	for vector,toReplaceList in vectorReplacementDict.items():							#Parse vector against the vcdbReplacement file
		for term in toReplaceList:
			for vec in vectorList:
				if vec == term: 
					if isinstance(vector, str) == False:
						vectorList.extend(vector)
					else:
						vectorList.append(vector)				
	for elem in vectorRemoveList:
		while elem in vectorList:
			vectorList.remove(elem)
	return vectorList				
		
def getVariety(JSONDict): #action.error.variety action.hacking.variety action.malware.variety action.misuse.variety action.physical.variety action.social.variety are lists
	varietyList = []
	if action in JSONDict:
		for type in fieldsList:
			if type in JSONDict[action]:
				if variety in JSONDict[action][type]:
					varietyList.extend(JSONDict[action][type][variety])				#Extend to include list into varietyList
	if attribute in JSONDict:														#attribute.availability.variety is a list
		if availability in JSONDict[attribute]:
			if variety in JSONDict[attribute][availability]:
				varietyList.extend(JSONDict[attribute][availability][variety])		#Extend to include list into varietyList		
	return parseVarietyList(varietyList)										    #Only return when varietyList has elements

def parseVarietyList(varietyList):													#Remove wrong varieties from the variety list in the vcdbReplacement file
	for elem in varietyRemoveList:
		while elem in varietyList:
			varietyList.remove(elem)
	return varietyList		

def parseToolList(fullList):														#Parse tool against the vcdbReplacement file
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
	
def parseVulnerabilityList(fullList):												#Parse vulnerability against the vcdbReplacement file
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
	
def parseActionList(fullList):														#Parse action against the vcdbReplacement file
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

def addTVA(JSONDict):		#attribute.integrity.variety
	fullList = []
	if integrity in JSONDict[attribute]:											# Attribute field contains some TVA values
			if variety in JSONDict[attribute][integrity]:
				if hardwareTampering in JSONDict[attribute][integrity][variety]:
					fullList.append(hardwareTampering)
				elif softwareInstallation in JSONDict[attribute][integrity][variety]:
					fullList.append(softwareInstallation)
	fullList.extend(getVariety(JSONDict))
	fullList.extend(getVector(JSONDict))
	return parseList(parseToolList(fullList)),parseList(parseVulnerabilityList(fullList)),parseList(parseActionList(fullList))	#Return TVA


def addUnAuthResult(JSONDict,actionList): #action.hacking.result action.malware.result action.misuse.result action.physical.result action.social.result are lists
	unAuthList = []
	if action in JSONDict:
		for type in fieldsList:
			if type in JSONDict[action]:
				if result in JSONDict[action][type]:
					unAuthList.extend(JSONDict[action][type][result])				#Extend to include list into unAuthList	
	if actionList != nullValue:
		for elem in actionList:
			if elem == "Loss" or elem == "Theft":									#Parse action list
				unAuthList.append("Theft of Resources")
			if elem == "DoS" or elem == "Interruption" or elem == "Degradation":
				unAuthList.append("Denial of Service")
	unAuthList.extend(getRecordsAction(JSONDict))									#If data is disclosed, it is an unauthorized result
	return parseList(parseUnAuthList(unAuthList))									#Only return when unAuthList has elements

def getRecordsAction(JSONDict): #attribute.integrity.variety attribute.confidentiality.data_disclosure are str 
	recActList = []
	if attribute in JSONDict:
		if integrity in JSONDict[attribute]:
			if variety in JSONDict[attribute][integrity]:
				recActList.extend(JSONDict[attribute][integrity][variety])
		if confidentiality in JSONDict[attribute]:
			if data_disclosure in JSONDict[attribute][confidentiality]:
				if JSONDict[attribute][confidentiality][data_disclosure] != Unknown:
					if JSONDict[attribute][confidentiality][data_disclosure] == Yes:
						recActList.append("Disclosed")								#If data is disclosed, it is an unauthorized result
		return recActList

def parseUnAuthList(unAuthList):
	for unAuth,toReplaceList in unAuthResultReplacementDict.items():				#Parse unauthorized results against the vcdbReplacement file
		for term in toReplaceList:
			for una in unAuthList:
				if una == term: 
					unAuthList.append(unAuth)				
	for elem in unAuthResultRemoveList:
		while elem in unAuthList:
			unAuthList.remove(elem)
	return unAuthList	

def addRecordsAffected(JSONDict): #attribute.confidentiality.data_total is a str
	if attribute in JSONDict:
		if confidentiality in JSONDict[attribute]:
			if data_total in JSONDict[attribute][confidentiality]:
					return JSONDict[attribute][confidentiality][data_total]

def getRecordsType(JSONDict): #attribute.confidentiality.data.variety attribute.confidentiality.data_victim attribute.confidentiality.state are lists
	recordTypeList = []
	if attribute in JSONDict:
		if confidentiality in JSONDict[attribute]:
			if data in JSONDict[attribute][confidentiality]:
				if variety in JSONDict[attribute][confidentiality][data]:
					recordTypeList.extend(JSONDict[attribute][confidentiality][data][variety])	#Extend to include list into recordTypeList
	if attribute in JSONDict:
		if confidentiality in JSONDict[attribute]:
			if data_victim in JSONDict[attribute][confidentiality]:
				recordTypeList.extend(JSONDict[attribute][confidentiality][data_victim])		#Extend to include list into recordTypeList	
	if attribute in JSONDict:
		if confidentiality in JSONDict[attribute]:
			if state in JSONDict[attribute][confidentiality]:
				recordTypeList.extend(JSONDict[attribute][confidentiality][state])				#Extend to include list into recordTypeList
	return recordTypeList																		#Only return when recordTypeList has elements

def addAssetsAffected(JSONDict):#asset.total_amount is an integer
	if asset in JSONDict:
		if total_amount in JSONDict[asset]:
			return JSONDict[asset][total_amount]

def getAssetsType(JSONDict):#asset.assets.variety is a list of strings where the elements have letters append like 'M - Document' asset.management asset.ownership are lists
	assetTypeList = []
	if asset in JSONDict:
		if assets in JSONDict[asset]:
			if variety in JSONDict[asset][assets][0]:
				if JSONDict[asset][assets][0][variety] != Unknown and JSONDict[asset][assets][0][variety] != other:
					parsed = JSONDict[asset][assets][0][variety].split(" - ")[1].strip()				#Split the strings to get the assets
					assetTypeList.append(parsed)
		if management in JSONDict[asset]:
			assetTypeList.extend(JSONDict[asset][management])											#Extend to include list into assetTypeList
		if ownership in JSONDict:
			assetTypeList.extend(JSONDict[asset][ownership])											#Extend to include list into assetTypeList
		return assetTypeList																			#Only return when assetTypeList has elements

def parseTargetedList(targetedList):
	for target,toReplaceList in targetReplacementDict.items():											#Parse target against the vcdbReplacement file
		for term in toReplaceList:
			for tar in targetedList:
				if tar == term: 
					targetedList.append(target)				
	for elem in targetRemoveList:
		while elem in targetedList:
			targetedList.remove(elem)
	return targetedList	

def addTargeted(JSONDict):																				#Obtain targeted
	targetedList = []
	targetedList.extend(getRecordsType(JSONDict))
	targetedList.extend(getAssetsType(JSONDict))
	return parseList(parseTargetedList(targetedList))

def addTarget(JSONDict):																				#Return target dict
	targetDict = {"targeted" : addTargeted(JSONDict), "records_affected" : addRecordsAffected(JSONDict), "assets_affected" : addAssetsAffected(JSONDict)}
	return targetDict
	
def addCurrencyAndMonetaryLoss(JSONDict,dateDict):#impact.iso_currency_code impact.overall_amount impact.overall_max_amount are float values
	if impact in JSONDict:
		#Declare null values
		originalCurrency = nullValue
		originalAmount = nullValue
		estimatedAmount = nullValue
		convertedAmount = nullValue
		#Assign values to variables if they are present
		if iso_currency_code in JSONDict[impact]:
			originalCurrency = JSONDict[impact][iso_currency_code]						
		if overall_amount in JSONDict[impact]:
			originalAmount = JSONDict[impact][overall_amount]
		if overall_max_amount in JSONDict[impact]:
			estimatedAmount = JSONDict[impact][overall_max_amount]
		if originalCurrency != nullValue: 														#If the currency is not null
			if originalAmount != nullValue:
				convertedAmount = convertToUSD(originalAmount,originalCurrency,dateDict)		#Convert the amount to USD
			elif estimatedAmount != nullValue:
				convertedAmount = convertToUSD(estimatedAmount,originalCurrency,dateDict)		#Convert the amount to USD
		if originalCurrency == nullValue:														#If there is no currency
			return nullValue						
		else:
			if estimatedAmount != nullValue:
				monetaryLossDict = {"original_currency" : originalCurrency, "unconverted" : estimatedAmount, "currency" : currencyUSD, "amount" : convertedAmount, isEstimate : Yes}#Estimated
				return monetaryLossDict
			else:
				monetaryLossDict = {"original_currency" : originalCurrency, "unconverted" : originalAmount, "currency" : currencyUSD, "amount" : convertedAmount, isEstimate : checkMonetaryLossThreshold(convertedAmount)}#Normal
				return monetaryLossDict
	else:
		return nullValue

def convertToUSD(amt,currency,dateDict):										#Convert the amount to USD at the time of incident
	if currency == currencyUSD :												#If value already in USD, it does not need conversion
		return amt
	else:
		curYear = dateDict[year]
		curMonth = dateDict[month]
		curDay = dateDict[day]
		if currency in cc.currencies:
			if curYear != nullValue and curMonth != nullValue and curDay != nullValue:
				try:
					return round(cc.convert(amt, currency, currencyUSD, date=datetime(curYear,curMonth,curDay)),2)
				except:
					return amt * mp.ratesAgainstUSD[currency]
			else:
				try:
					return round(cc.convert(amt, currency, currencyUSD, date=datetime(curYear,6,15)),2)				#Take middle of the year if the date does not contain the month or day
				except:
					return amt * mp.ratesAgainstUSD[currency]

def checkMonetaryLossThreshold(amt):															#Check if monetary loss exceeds threshold for estimated value
	if amt > monetaryLossThreshold:
		return Yes
	else:
		return No

def addDiscovered(JSONDict):# discovery_method.external.variety discovery_method.internal.variety discovery_method.other discovery_method.partner.variety are lists
	discList = []
	if discovery_method in JSONDict:
		if external in JSONDict[discovery_method]:
			if variety in JSONDict[discovery_method][external]:
				discList.extend(JSONDict[discovery_method][external][variety])
	if discovery_method in JSONDict:
		if internal in JSONDict[discovery_method]:
			if variety in JSONDict[discovery_method][internal]:
				discList.extend(JSONDict[discovery_method][internal][variety])
	if discovery_method in JSONDict:
		if partner in JSONDict[discovery_method]:
			if variety in JSONDict[discovery_method][partner]:
				discList.extend(JSONDict[discovery_method][partner][variety])
	return parseList(discList)																#Only return when discList has elements

def addDescription(JSONDict): #control_failure + summary are str
	fullDesc = ""
	if control_failure in JSONDict:
		fullDesc = JSONDict[control_failure].capitalize() 				#Control failure has a description and is important as well. The first word should be capitalized before assignment.
	if summary in JSONDict:
		if fullDesc != "":
			fullDesc = fullDesc + "\n" + JSONDict[summary].capitalize() #Concat a breakline. The first word should be capitalized before assignment.
		else:
			fullDesc = JSONDict[summary].capitalize()					#The first word should be capitalized before assignment.
	if fullDesc != "":
		return fullDesc
	else:
		return nullValue

def addInfoSource(JSONDict): #plus.analyst plus.investigator are str
	infoList = []
	if plus in JSONDict:
		if analyst in JSONDict[plus]:
			infoList.append(JSONDict[plus][analyst])
		if investigator in JSONDict[plus]:
			infoList.append(JSONDict[plus][investigator])
	if len(infoList) >= 1:
		return infoList
	else:
		return nullValue
	
def addSourceLink(JSONDict): #reference is a str with a single url or with urls separated by ; or ,
	urlList = []
	purlList = []
	if reference in JSONDict:
		if ";" in JSONDict[reference]:
			urlList = JSONDict[reference].split(";")				#Split by ; to a url list
		elif "," in JSONDict[reference]:
			urlList = JSONDict[reference].split(",")				#Split by , to a url list
		else:
			urlList.append(JSONDict[reference])						#Return single url in a list
		if len(urlList) >= 1:
			for url in urlList:
				purlList.append(url.replace(' ',''))				#Remove whitespaces
			return parseSourceLink(purlList)
		else:
			return nullValue

def parseSourceLink(sList):											#Remove empty urls
	if "" in sList:
		sList.remove("")
	return sList	

def addValues(JSONDict,parseDict):
	#parseDict[0] = vcdb 																							#Always type
	parseDict["description"] = addDescription(JSONDict)																#Description
	parseDict["incident_date"] = addIncidentDate(JSONDict)															#Dates
	parseDict["resolution_date"] = addResolutionDate(JSONDict,parseDict["incident_date"])
	parseDict["notification_date"] = addNotificationDate(JSONDict)
	parseDict["entry_date"] = addEntryDate(JSONDict)
	parseDict["victim"] = addVictim(JSONDict)																		#victim
	parseDict["industry"] = addIndustry(JSONDict)																	#industry
	parseDict["country"] = addCountry(JSONDict)																		#country
	parseDict["state"] = addState(JSONDict)																			#location
	parseDict["employee_count"] = addEmpCount(JSONDict)																#employee count
	parseDict["attacker"] = addAttackerToDict(JSONDict,getRecordsAction(JSONDict),parseDict["description"])			#attacker name, origin and role
	parseDict["objectives"] = addObjectives(JSONDict)																#objectives
	parseDict["discovered_by"] = addDiscovered(JSONDict)															#Discovered By
	parseDict["cve"] = addCVE(JSONDict)																				#CVE
	parseDict["malware_used"] = addMalware(JSONDict)																#Malware
	parseDict["tool"],parseDict["vulnerability"],parseDict["action"] = addTVA(JSONDict)								#Tool Vulnerability and Action
	parseDict["unauthorized_result"] = addUnAuthResult(JSONDict,parseDict["action"])								#Unauthorized Result	
	parseDict["target"] = addTarget(JSONDict)																		#Target	
	parseDict["monetary_loss"] = addCurrencyAndMonetaryLoss(JSONDict,parseDict["incident_date"])
	parseDict["info_source"] = addInfoSource(JSONDict)																#Info Source
	parseDict["source_link"] = addSourceLink(JSONDict)																#Source Link
	return parseDict