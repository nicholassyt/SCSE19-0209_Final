import pymongo

def getCollectionNames(db):
	return db.list_collection_names()

def doDrop(db,dropList):
	isDropped = False
	try:
		for col in dropList:										#Loop for all the collections in collectionsList
			db[col].drop()											#Open collection and execute drop command
		isDropped = True
		return isDropped
	except:
		return isDropped