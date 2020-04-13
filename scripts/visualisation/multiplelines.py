import json

#Dictionary to that has the key as year and the value to be set
valueByYearDict = {2010 : 0, 2011 : 0, 2012 : 0, 2013 : 0, 2014 : 0, 2015 : 0, 2016 : 0, 2017 : 0, 2018 : 0, 2019 : 0}

def getDictOfLists(jsonList,predType,predTypeList):
	dictOfLists = {}
	predType = list(jsonList[0].values())[0]													#The predType is the first value in the jsonList
	try:
		for dict in jsonList:
			if predType == predTypeList[0] or predType == predTypeList[2]: 						#If the predType matches the type defined in predTypeList
				key = dict["tool"]
				value = getCountByYearList(dict["aggregateList"])
			elif predType == predTypeList[1] or predType == predTypeList[12] or predType == predTypeList[15]: 
				key = dict["industry"]
				value = getCountByYearList(dict["aggregateList"])
			elif predType == predTypeList[4] or predType == predTypeList[5]: 
				key = dict["tool"]
				value = getMonetaryAmountByYearList(dict["aggregateList"])
			elif predType == predTypeList[3] or predType == predTypeList[6]: 
				key = dict["industry"]
				value = getMonetaryAmountByYearList(dict["aggregateList"])
			elif predType == predTypeList[7] or predType == predTypeList[10]: 
				key = dict["industry"]
				value = getDataRecordsByYearList(dict["aggregateList"])
			elif predType == predTypeList[8] or predType == predTypeList[9]: 
				key = dict["tool"]
				value = getDataRecordsByYearList(dict["aggregateList"])
			elif predType == predTypeList[11] or predType == predTypeList[13]: 
				key = dict["objectives"]
				value = getCountByYearList(dict["aggregateList"])
			elif predType == predTypeList[14] or predType == predTypeList[16]:
				key = dict["unauthorized_result"]
				value = getCountByYearList(dict["aggregateList"])
			dictOfLists.update({key : value})
		return dictOfLists
	except Exception as e:
		print(e)

def getCountByYearList(countList):							#Set the value of the key, which is year
	localValueDict = valueByYearDict.copy()					#Copy the dict that has 0 as a value for each key
	for dict in countList:
		for year, count in localValueDict.items():	
			if dict["year"] == year:
				localValueDict[year] = dict["count"]		#Set year field with the value from count
	return list(localValueDict.values())
	
def getMonetaryAmountByYearList(amtList):
	localValueDict = valueByYearDict.copy()
	for dict in amtList:
		for year, amt in localValueDict.items():
			if dict["year"] == year:
				localValueDict[year] = dict["lossAmt"]		#Set year field with the value from lossAmt
	return list(localValueDict.values())
	
def getDataRecordsByYearList(amtList):
	localValueDict = valueByYearDict.copy()
	for dict in amtList:
		for year, amt in localValueDict.items():
			if dict["year"] == year:
				localValueDict[year] = dict["dataRecords"]	#Set year field with the value from dataRecords
	return list(localValueDict.values())

def parseMulLineData(jsonList,predType,predTypeList):
	return getDictOfLists(jsonList,predType,predTypeList)	#Function that is called by the visualisation file

def getYearList():											#Get year list
	return list(valueByYearDict.keys())