import json
import os
import pymongo 
import dateutil.parser

#Declarations
JSONFileFolder = os.path.join(os.path.dirname(__file__), "mergeSchema/json_merged")
#JSONFileFolder = os.path.join(os.path.dirname(__file__), "jsons/")
dateList = ["incident_date","resolution_date","notification_date","entry_date"]

class Decoder(json.JSONDecoder):																		#Decoder to parse strings with numbers into int values
    def decode(self, s):
        result = super().decode(s)  
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o

def parseDatesToISODate(json_data):																		#Dates have to be parsed to ISO date with dateutil
	for line in json_data:
		for dateField in dateList:
			if line[dateField] != None:
				if line[dateField]["date"] != None:
					line[dateField]["date"] = dateutil.parser.parse(line[dateField]["date"])

def parsingFunctions(json_data,col):
	parseDatesToISODate(json_data)

def openFileAndStore(fileName,collection,col):
	try:
		with open(fileName, encoding='utf-8') as data:													#File must be opened with utf-8 encoding as there are symbols errors without it
			json_data = json.load(data,cls=Decoder)														#Call json.load to load json data. The decoder class parses strings with numbers into int values.
		data.close()
		parsingFunctions(json_data,col)
		result = collection.insert_many(json_data)														#Call pymongo insert_many to insert multiple documents
	except Exception as e: 
		print(e)
		quit()

def getJSONFiles():
	jf = JSONFileFolder.replace("\mongo","")
	JSONFiles = [os.path.join(r,file) for r,d,f in os.walk(jf) for file in f]							#Get the files should in the JSON folder
	return JSONFiles

def getJSONstored():																					#Return the files that have been stored into mongoDB
	jsonFileList = getJSONFiles()
	returnList = []
	for jsonFile in jsonFileList:
		returnList.append(jsonFile.split("\\")[-1])
	return returnList
	
def getCollectionNames(db):
	return db.list_collection_names()																	#Return a list of collections in the database

def doStore(db):
	isStored = False
	try:
		JSONFiles = getJSONFiles()
		for fileName in JSONFiles :																		#Loop for all the collections in collectionsList
			col = fileName.split("\\")[-1].split(".")[0]															
			collection = db[col]																		#Store db[col] as collection variable
			openFileAndStore(fileName,collection,col)													#Pass the file name and collection to store function
		collection.create_index([("$**", pymongo.TEXT)], name="TextIndex", default_language="english") 	#Create text index to facilitate search using query = { "$text" : { "$search" : word }}
		isStored = True
		return isStored																		
	except:
		return isStored