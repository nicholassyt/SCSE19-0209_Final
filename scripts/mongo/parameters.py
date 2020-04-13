#Declaration of file extensions
JSONEXT = ".json"
TXTEXT = ".txt"

#PyMongo Connection
DBName = "Incidents"												#Database that holds the various cyber security incidents						
atlasExamples = ["l0uqk", "scse19-0209", "nicholassyt"]
onlineExamples = ["13.250.96.171", "27017", DBName ,"nicholassyt"]

#Collections defined and stored in a string list
SCSE19_0209 = "SCSE19_0209"											#Merges schema into this collection
collectionsList = [SCSE19_0209] 	 								#List of collections to be iterated	

ratesAgainstUSD = {"GBP" : 1.22, "EUR" : 1.10, "ZAR" : 0.065, "INR" : 0.014, "THB" : 0.033, "KRW" : 0.00083, "CAD" : 0.75, "AUD" : 0.67, "CZK" : 0.043}