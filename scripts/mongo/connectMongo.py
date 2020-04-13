import pymongo 
import scripts.mongo.parameters as parameters

#Declarations
mongoDBLocalConnection = "mongodb://localhost"
DBName = parameters.DBName

def doLocalConnection():
	connection = pymongo.MongoClient(mongoDBLocalConnection)																#Connects to the local instance of MongoDB
	return connection[DBName]	
	
def doAtlasConnection(hostingServer,clusterID,userID,password):																#Defines the MongoDB Atlas connection URL
	mongoDBConnection = "mongodb+srv://" + userID + ":" + password + "@" + clusterID + "-" + hostingServer + ".mongodb.net/test?retryWrites=true"
	connection = pymongo.MongoClient(mongoDBConnection)																		#Connects to MongoDB Atlas
	return connection[DBName]																								#Setup connection to the desired database

def doOnlineConnection(serverIP,portNum,dbName,userID,password):															#Defines the MongoDB connection URL
	mongoDBConnection = "mongodb://" + userID + ":" + password + "@" + serverIP + ":" + portNum + "/" + dbName	
	connection = pymongo.MongoClient(mongoDBConnection)																		#Connects to the online instance of MongoDB
	return connection[DBName]																								#Setup connection to the desired database

def doOnlineConnectionIP(fullIP):																							#Defines the MongoDB connection URL
	connection = pymongo.MongoClient(fullIP)																				#Connects to the online instance of MongoDB
	return connection[DBName]																								#Setup connection to the desired database		