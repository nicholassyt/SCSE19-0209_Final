import os

#Constants for saving the image that is displayed by the interface
uploadFolder = 'UPLOAD_FOLDER'
imageFolder = os.path.join('static', 'images')
clusteringImage = "clusteringImage.png"
elbowImage = "elbowImage.png"
regressionImage = "regressionImage.png"
graphImage = "graphImage.png"

#Functions to return the image folder and image name
def assignConfig(app):
	app.config[uploadFolder] = imageFolder

def getGraphImageLocation():
	return imageFolder + "/" + graphImage

def getElbowImageLocation():
	return imageFolder + "/" + elbowImage

def getClusteringImageLocation():
	return imageFolder + "/" + clusteringImage
	
def getRegressionImageLocation():
	return imageFolder + "/" + regressionImage

def getGraphJSONFile(graphJSONFile):
	#graphJSONFile = "\\files_to_select\\" + graphJSONFile
	return os.path.join(os.path.dirname(__file__), graphJSONFile)

#Functions can be called to retrieve the files for clustering or regression
def getClusteringJSONFile():
	return os.path.join(os.path.dirname(__file__), "Ransomware.json")

def getRegressionJSONFile():
	return os.path.join(os.path.dirname(__file__), "Finance.json")

def getMappingFile():
	return os.path.join(os.path.dirname(__file__), "mapping.txt")

# def getElbowImage(app):
	# return elbIm
	# #return os.path.join(app.config[uploadFolder], elbIm)

# def getClusteringImage(app):
	# return clusIm
	
# def getRegressionImage(app):
	# return regIm