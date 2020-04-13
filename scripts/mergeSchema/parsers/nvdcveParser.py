import dateutil.parser
import  scripts.mergeSchema.mergeParameters as mp

# Declarations
nullValue = mp.nullValue
No = "No"
nvdcveType = "nvdcve"
publishedDate = "publishedDate"
cve = "cve"
affects = "affects"
vendor = "vendor"
vendor_data = "vendor_data"
vendor_name = "vendor_name"
product = "product"
product_data = "product_data"
product_name = "product_name"
CVE_data_meta = "CVE_data_meta"
ID = "ID"
impact = "impact"
baseMetricV3 = "baseMetricV3"
cvssV3 = "cvssV3"
cvssV2 = "cvssV2"
baseMetricV2 = "baseMetricV2"
attackVector = "attackVector"
accessVector = "accessVector"
description = "description"
description_data = "description_data"	
value = "value"
references = "references"
reference_data = "reference_data"
url = "url"

date = "date"
day = "day"
month = "month"
year = "year"
date_isEstimate = "date_isEstimate"

def addEntryDate(JSONDict): #publishedDate
	if publishedDate in JSONDict:		
		dt = dateutil.parser.parse(JSONDict[publishedDate])															#Dates have to be parsed to ISO date
		return 	{date : dt, year : dt.year, month : dt.month, day : dt.day, date_isEstimate : No}

# The victim value may be found in various fields and these are added to a list
def addVictim(JSONDict): #cve.affects.vendor.vendor_data.vendor_name cve.affects.vendor.vendor_data.product.product_data.product_name
	victimList = []
	if cve in JSONDict:
		if affects in JSONDict[cve]:
			if vendor in JSONDict[cve][affects]:
				if vendor_data in JSONDict[cve][affects][vendor]:
					if len(JSONDict[cve][affects][vendor][vendor_data]) >= 1:
						if vendor_name in JSONDict[cve][affects][vendor][vendor_data][0]: #list 
							victimList.append(JSONDict[cve][affects][vendor][vendor_data][0][vendor_name])
							if product in JSONDict[cve][affects][vendor][vendor_data][0]:
								if product_data in JSONDict[cve][affects][vendor][vendor_data][0][product]:
									i = 0
									while i != len(JSONDict[cve][affects][vendor][vendor_data][0][product][product_data]): #list 
										if product_name in JSONDict[cve][affects][vendor][vendor_data][0][product][product_data][i]:
											victimList.append(JSONDict[cve][affects][vendor][vendor_data][0][product][product_data][i][product_name])
											i+=1
						return victimList

# The CVE id is important
def addCVE(JSONDict): #cve.CVE_data_meta.ID
	if cve in JSONDict:
		if CVE_data_meta in JSONDict[cve]:
			if ID in JSONDict[cve][CVE_data_meta]:
				return [JSONDict[cve][CVE_data_meta][ID]]

# The vulnerability value may be found in various fields and these are added to a list
def addVulnerability(JSONDict): #impact.baseMetricV3.cvssV3.attackVector impact.baseMetricV2.cvssV2.accessVector
	vectorList = []
	if impact in JSONDict:
		if baseMetricV3 in JSONDict[impact]:
			if cvssV3 in JSONDict[impact][baseMetricV3]:
				if attackVector in JSONDict[impact][baseMetricV3][cvssV3]:
					vectorList.append(JSONDict[impact][baseMetricV3][cvssV3][attackVector])
					return vectorList
		if baseMetricV2 in JSONDict[impact]:
			if cvssV2 in JSONDict[impact][baseMetricV2]:
				if accessVector in JSONDict[impact][baseMetricV2][cvssV2]:
					vectorList.append(JSONDict[impact][baseMetricV2][cvssV2][accessVector])
					return vectorList

def addDescription(JSONDict): #cve.description.description_data.value
	if cve in JSONDict:
		if description in JSONDict[cve]:
			if description_data in JSONDict[cve][description]:
				if value in JSONDict[cve][description][description_data][0]:
					return JSONDict[cve][description][description_data][0][value]

def addSourceLink(JSONDict): #cve.references.reference_data.url
	slList = []
	if cve in JSONDict:
		if references in JSONDict[cve]:
			if reference_data in JSONDict[cve][references]:
				i = 0
				while i != len(JSONDict[cve][references][reference_data]): #list of dictionaries
					if url in JSONDict[cve][references][reference_data][i]:
						slList.append(JSONDict[cve][references][reference_data][i][url])
						i+=1
				return slList		

def addValues(JSONDict,parseDict):
	#parseDict[0] = nvdcve																					#Always type 
	parseDict["resolution_date"] = nullValue
	parseDict["incident_date"] = nullValue
	parseDict["notification_date"] = nullValue
	parseDict["entry_date"] = addEntryDate(JSONDict)														#Dates
	parseDict["victim"] = addVictim(JSONDict)																#victim
	parseDict["cve"] = addCVE(JSONDict)																		#CVE
	parseDict["vulnerability"] = addVulnerability(JSONDict)													#Vulnerability
	parseDict["attacker"] = nullValue
	parseDict["monetary_loss"] = nullValue
	parseDict["description"] = addDescription(JSONDict)														#Description
	parseDict["source_link"] = addSourceLink(JSONDict)														#Source Link
	return parseDict