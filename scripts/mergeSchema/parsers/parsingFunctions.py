import sys

# Parsers must be imported accordingly
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.prdbParser as prp
import scripts.mergeSchema.parsers.vcdbParser as vcp
import scripts.mergeSchema.parsers.nvdcveParser as nvdcve
import scripts.mergeSchema.parsers.healthParser as hp
import scripts.mergeSchema.parsers.risiParser as rp
import scripts.mergeSchema.parsers.wikiParser as wp

# Importing the example parser
# import scripts.mergeSchema.parsers.exampleParser as ep

# To enable the use of global values
thismodule = sys.modules[__name__]
thismodule.previousId = 0

def update_previousId(i):
	thismodule.previousId = i	#tracks the id number

def getParsedJSONDict(JSONDict,parseDict,dbType,i):								
	parseDict["typeId"] = dbType + "-" + str(i)								#appends an id number to the type		
	if dbType == mp.prdbType:
		return prp.addValues(JSONDict,parseDict)
	elif dbType == mp.vcdbType:
		return vcp.addValues(JSONDict,parseDict)
	elif dbType == mp.nvdcveType:
		return nvdcve.addValues(JSONDict,parseDict)
	elif dbType == mp.healthType:
		return hp.addValues(JSONDict,parseDict)
	elif dbType == mp.risiType:
		return rp.addValues(JSONDict,parseDict)
	elif dbType == mp.wikiType:
		return wp.addValues(JSONDict,parseDict)
		
	# The type should be defined in the merge parameters file	
	#elif dbType == mp.exampleType:
		#return ep.addValues(JSONDict,parseDict)

def parseJSON(json_data,dbType):#json_data is list of dictionaries																					
	#Declarations of empty List and the Dictionary to reference
	parsedJSON = []
	parseAgainst = mp.fieldsToAdd
	i = 0
	
	if dbType == mp.nvdcveType:												#nvdcve has multiple files and the id needs to be tracked when the next json file is called
		i = previousId

	for JSONDict in json_data:												#For each Dict in json_data	
		parseDict = parseAgainst.copy()										#Copy is required as an assignment is just a pointer to the original dict
		parsedJSONDict = getParsedJSONDict(JSONDict,parseDict,dbType,i)		#Retrieve the relevant values from the JSON dict and store to the new Dict
		if list(parsedJSONDict.values())[4] != mp.nullValue or parsedJSONDict != mp.nullValue:				#If there is no date, do not append the incident
			parsedJSON.append(parsedJSONDict)
			i+=1
	
	if dbType == mp.nvdcveType:												#nvdcve has multiple files and the id needs to be tracked when the next json file is called
		update_previousId(i)
	
	return parsedJSON														#Return the parsed json file