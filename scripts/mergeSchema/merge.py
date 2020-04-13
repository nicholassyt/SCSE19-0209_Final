#Imports
import json
import os, sys, subprocess
from datetime import datetime
import scripts.mergeSchema.mergeParameters as mp
import scripts.mergeSchema.parsers.parsingFunctions as pf

#File path constants
JSONToMergeFolder = mp.JSONToMergeFolder
JSONMergedFolder = mp.JSONMergedFolder

#JSON files
prdbFileName = mp.prdbFileName
vcdbFileName = mp.vcdbFileName
healthFileName = mp.healthFileName
risiFileName = mp.risiFileName
wikiFileName = mp.wikiFileName
JSONMergedFileName = mp.JSONMergedFileName

def parsingFunctions(json_data,jsonFileName):														#Add new parsing functions to this function
	dbType = None
	if jsonFileName == prdbFileName:																#Parsing the various JSON files
		dbType = mp.prdbType
	elif jsonFileName == vcdbFileName:																
		dbType = mp.vcdbType
	elif mp.nvdcveType in jsonFileName:																#nvdcve has multiple files and needs to be parsed based on type
		dbType = mp.nvdcveType
	elif jsonFileName == healthFileName:
		dbType = mp.healthType
	elif jsonFileName == risiFileName:
		dbType = mp.risiType
	elif jsonFileName == wikiFileName:
		dbType = mp.wikiType
	# elif jsonFileName == exampleFileName:
		# dbType = mp.exampleType
	if dbType != None:
		return pf.parseJSON(json_data,dbType)

#########################################################################################The Decoder Classes are defined here###########################################################################################################
class Decoder(json.JSONDecoder):																	#Decoder to parse strings with numbers into int values
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
			
class dateTimeEncoder(json.JSONEncoder):															#Decoder to allow for printing datetime as a string
	def default(self, obj):
		if isinstance (obj, datetime): 
			return str(obj.isoformat())
		elif isinstance (obj, datetime.date):
			return str(obj.isoformat())
		return json.JSONEncoder.default(self, obj)
#########################################################################################The Encoder Classes are defined here###########################################################################################################

#########################################################################################The File Merging Code is defined here###########################################################################################################

def getJSONFiles(folder):
	JSONFiles = [os.path.join(r,file) for r,d,f in os.walk(folder) for file in f]					#Store all files in specified directory to a list
	return JSONFiles

def getJSONFileNames():																				#Parse filenames in list by getting only the last substr after splitting by '/'
	jf = getJSONFiles(JSONToMergeFolder)
	splitList = []
	for f in jf:
		splitList.append(f.rsplit('/')[1])
	return splitList	

def openFilesAndParseData(JSONFiles):
	jsonList = []
	#dupList = []
	i = 0
	print("Start merging")
	prepareFile(JSONMergedFileName)																	#Prepare merged file
	while i != len(JSONFiles):
		print("Merging " + JSONFiles[i].split("/")[-1]	 + " now")
		json_data = parsingFunctions(getJSONData(JSONFiles[i]),JSONFiles[i])						#Parse JSON data by adding or removing fields
		if json_data != None:
			for line in json_data:
				jsonList.append(json.dumps(line,cls=dateTimeEncoder))								#To allow for the printing of double quotes and datetime
		#dupList.extend(jsonList)
			appendToJSONFile(jsonList,i,len(JSONFiles))
			jsonList = []
		i+=1
	appendFileEnd(JSONMergedFileName)
	print("Merge Completed")

def getJSONData(fileName):
	with open(fileName, encoding='utf-8') as data:													#File must be opened with utf-8 encoding as there are symbols errors without it
		json_data = json.load(data,cls=Decoder)														#Call json.load to load json data. The decoder class parses strings with numbers into int values.
	data.close()
	return json_data

def appendToJSONFile(json_data,currentFileCount,numOfFiles):
	lineCount = 0
	with open(JSONMergedFileName, 'a', encoding='utf-8') as f:										#'a' is used to append queries to the same json file, encoding required to print VERIS queries
		for line in json_data:
			print (line, file = f,end = '')
			if currentFileCount == numOfFiles-1 and lineCount == len(json_data)-1:					#If it is the last entry in the json merging do not append a comma
				continue
			else:
				print (",", file = f)																#Print a comma for each line
			lineCount += 1
	f.close()

def checkDuplicates(json_data): 																	#Check for duplicates 
	finalList = []
	nvdcveList = []
	seen = set()
	boolFirst = True
	print("Checking for duplicates")
	try:
		if json_data != None:
			for left in json_data:
				didNotMerge = True
				if "nvdcve" not in left["typeId"]:													#Skip nvdcve as they should not have duplicates
					for right in json_data:
						if isDuplicate(left,right,seen):											
							mergedDict = mergeIfDuplicate(left,right)
							if mergedDict:#Only append if mergedDict is not None
								finalList.append(mergedDict)
								seen.add(right["typeId"])
								didNotMerge = False
							else:
								didNotMerge = True
								
					if didNotMerge and left["typeId"] not in seen:#If merge is not and the id is not present in seen
						finalList.append(left)
				else:
					nvdcveList.append(left)
	except e:
		print(e)
	#Print values to determine what has been removed after checking for duplicates
	print("Finished checking for duplicates")	
	print(seen)
	print("length number of duplicates: " + str(len(seen)))
	print("length total data: " + str(len(json_data)))
	print("length after remove dup: " + str(len(finalList)))
	return [dict(t) for t in {tuple(d.items()) for d in finalList}].extend(nvdcveList) #Final duplicate removal

def isDuplicate(left,right,seen):
	if left != right and left["typeId"] not in seen: 												#Check if is a duplicate based on various factors
		if left["entry_date"] == right["entry_date"] and left["victim"] == right["victim"] and left["info_source"] == right["info_source"] and left["country"] == right["country"]:
			return True
	else:
		return False

def mergeIfDuplicate(left,right):																	#Merge values if it is a duplicate and the value is None
	if left != right:
		if left["entry_date"] == right["entry_date"] and left["victim"] == right["victim"]:
			for key, value in left.items():
				if value is None:
					if right[key] is not None:
						value = right[key]
				left[key] = value
			return left		

def saveToJSONFile(finalList):
	length = len(finalList)
	i = 0
	with open(JSONMergedFileName, 'w', encoding='utf-8') as f:										#'w' is used to write json file, encoding required to print VERIS queries
		print ("[", file = f)
		for dict in finalList:
			print (json.dumps(dict,cls=dateTimeEncoder), file = f,end = '')
			i+=1
			if i!=length:
				print (",", file = f)
		print ("]", file = f)	
	f.close()
	
def clearFileContents(fileName):																	#Function to clear file contents
	open(fileName, 'w').close()

def prepareFile(fileName):
	clearFileContents(fileName)
	with open(fileName, 'a', encoding='utf-8') as f:	
		print('[', file = f)																		#Append a '['
	f.close()
	
def appendFileEnd(fileName):
	with open(fileName, 'a', encoding='utf-8') as f:	
		print(']', file = f)																		#Append a ']'
	f.close()

def openFolder():																					#To open the folder containing the merged file after the merged has been completed
    if sys.platform == "win32":
        os.startfile(getFolderName())
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, getFolderName()])

def getFolderName():																				#Returns path to folder
	return os.path.realpath(JSONMergedFolder)
	
def doMerge():
	try :
		JSONFiles = getJSONFiles(JSONToMergeFolder)													#Get all JSON files in folder
		openFilesAndParseData(JSONFiles)															#Parse data in JSON files
		saveToJSONFile(checkDuplicates(getJSONData(JSONMergedFileName))) 							#Remove duplicates
		openFolder()																				#Open folder containing merged file
		return True
	except:
		return False
#########################################################################################The File Merging Code is defined here###########################################################################################################