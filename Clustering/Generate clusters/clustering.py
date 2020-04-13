import matplotlib
import json
import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing 
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

jsonFile = "data.json"
nullValue = None
null = "null"

def showMapping(df,le):
	mapping = dict(zip(le.classes_, range(0, len(le.classes_))))					#Can be called to print the mapping from the labelling
	print(mapping)

def getListOfDictFromJSONFile():													#JSON file is a list of dictionaries
	with open(jsonFile, 'r') as f:
		listOfDict = json.load(f)
	return listOfDict		

# def checkFieldsOne(adict):
	# if adict["country"] != nullValue and adict["industry"] != nullValue and adict["target"] != nullValue and adict["unauthorized_result"] != nullValue and adict["action"] != nullValue and adict["vulnerability"] != nullValue and adict["tool"] != nullValue and adict["objectives"] != None:
		# return True
# def checkFieldsTwo(adict):
	# if adict["industry"][0] != nullValue and adict["target"]["records_affected"] != nullValue and adict["unauthorized_result"][0] != nullValue and adict["action"][0] != nullValue and adict["vulnerability"][0] != nullValue and adict["tool"][0] != nullValue and adict["objectives"][0] != nullValue:
		# return True

# def findSuitableIncidents(lod):
	# suitableList = []
	# for adict in lod:
		# if checkFieldsOne(adict):
			# if checkFieldsTwo(adict):
				# dfDict = { "typeId" : adict["typeId"], "country" : adict["country"], "industry" :  adict["industry"][0], "action" : adict["action"][0] ,"unauth" : adict["unauthorized_result"][0], "vuln" : adict["vulnerability"][0], "tool" : adict["tool"][0], "objective" : adict["objectives"][0], "rec" : adict["target"]["records_affected"]}
				# suitableList.append(dfDict)
	# return suitableList

def findSuitableIncidents(lod):
	suitableList = []
	s = " "
	for adict in lod:
		industry = null
		country = null
		objectives = null
		tool = null
		vulnerability = null
		action = null
		records_affected = null
		unauthorized_result = null
		records_affected = null
		monetary_loss = null
		
		if adict["industry"] != nullValue:
			if isinstance(adict["industry"],list):
				industry = s.join(adict["industry"])
				
		if adict["country"] != nullValue:
			country = adict["country"]
	
		if adict["objectives"] != nullValue:
			if isinstance(adict["objectives"],list):
				objectives = s.join(adict["objectives"])
		
		if adict["tool"] != nullValue:
			if isinstance(adict["tool"],list):
				tool = s.join(adict["tool"])	
		
		if adict["vulnerability"] != nullValue:
			if isinstance(adict["vulnerability"],list):
				vulnerability = s.join(adict["vulnerability"])
		
		if adict["action"] != nullValue:
			if isinstance(adict["action"],list):
				action = s.join(adict["action"])	
		
		if adict["target"] != nullValue: 
			if adict["target"]["records_affected"] != nullValue:
				records_affected = adict["target"]["records_affected"]
				
		if adict["unauthorized_result"] != nullValue:
			if isinstance(adict["unauthorized_result"],list):
				unauthorized_result = s.join(adict["unauthorized_result"])

		if adict["monetary_loss"] != nullValue: 
			if adict["monetary_loss"]["amount"] != nullValue:
				monetary_loss = adict["monetary_loss"]["amount"]
		
		dfDict = { "typeId" : adict["typeId"], "country" : country, "industry" :  industry, "objectives" : objectives, "tool" : tool, "vulnerability" : vulnerability, "action": action, "records_affected" : records_affected, "unauthorized_result" : unauthorized_result, "monetary_loss" : monetary_loss }
		
		#dfDict = { "typeId" : adict["typeId"], "country" : adict["country"], "industry" :  adict["industry"][0], "action" : adict["action"][0] ,"unauth" : adict["unauthorized_result"][0], "action" : adict["action"][0], "vuln" : adict["vulnerability"][0], "tool" : adict["tool"][0], "objective" : adict["objectives"][0], "rec" : adict["target"]["records_affected"]}
		
		suitableList.append(dfDict)
	return suitableList


def encodeDF(df):
	le = preprocessing.LabelEncoder()
	for x in list(df.columns):
		df[x].fillna("null", inplace = True) 
	for x in list(df.columns):
		df[x] = df[x].astype('|S')
		df[x] = le.fit_transform(df[x]) # Encode labels in column
		#showMapping(df,le)
	return df

def doPCA(df,centroids):
	#Run PCA on the data and reduce the dimensions in pca_num_components dimensions
	#And allow for a plotting of a multi-dimensional graph in two dimensions
	pca_num_components = 2

	reduced_data = PCA(n_components=pca_num_components).fit_transform(df)
	reduced_centroids = PCA(n_components=pca_num_components).fit_transform(centroids)
	
	results = pd.DataFrame(reduced_data,columns=["pca1","pca2"])
	centroids_results = pd.DataFrame(reduced_centroids,columns=["pca1","pca2"])
	return results,centroids_results

def showElbow(df):														#Iterate the kmeans model 10 times to obtain the elbow graph
	wcss = []
	for i in range(1, 11):												
		kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)	
		kmeans.fit(df)
		wcss.append(kmeans.inertia_)
	plt.plot(range(1, 11), wcss)
	plt.title('Elbow Method')
	plt.xlabel('Number of clusters')
	plt.ylabel('WCSS')
	plt.show()
	
def main():
	lod = getListOfDictFromJSONFile()							#Get List of Dicts
	
	df = pd.DataFrame(findSuitableIncidents(lod))				#Find suitable incidents
	print(df)	
	tempDF = df.copy()											#Make a copy that has typeId for matching the clusters to the real labels
	df = df.drop(["typeId"],axis=1)								#Drop typeId as it should be involved in clustering
	df = encodeDF(df)											#Encode text to numeric values
	print(df)	
	data_scaled = normalize(df)									#Normalize values to improve analysis
	data_scaled = pd.DataFrame(data_scaled, columns=df.columns)	#Assign the normalized values
	print(data_scaled)
	
	showElbow(data_scaled)
	
	#Do Kmeans
	numOfClusters = 4
	clustering_kmeans = KMeans(n_clusters=numOfClusters, precompute_distances="auto", n_jobs=-1)
	data_scaled['cluster'] = clustering_kmeans.fit_predict(data_scaled)	#Add the predicted clusters to the dataframe
	centroids = clustering_kmeans.cluster_centers_						#Assign the centroids
	
	#Print the clustered data to csv files
	printDF = pd.concat([data_scaled, tempDF["typeId"]], axis=1)
	printDF = pd.merge(tempDF, printDF[["typeId","cluster"]], on="typeId",how="left")
	print(printDF)
	i = 0
	while i != numOfClusters:
		clusterFile = "cluster" + str(i) + ".csv"
		pd.DataFrame.to_csv(printDF[printDF.cluster == i], clusterFile)
		i+=1
	
	#Do PCA
	results,centroids_results = doPCA(data_scaled,centroids)
	print(results)
	print(centroids_results)
	
	#Plot the scatter plot with both the clusters and the centroids
	sns.set(style="whitegrid",palette="bright")
	fig, ax = plt.subplots()
	sns.scatterplot(x="pca1", y="pca2", hue=data_scaled['cluster'], data=results)
	
	ax2 = ax.twinx()
	g= sns.scatterplot(x="pca1", y="pca2", hue=range(len(centroids_results['pca1'])), data=centroids_results, s=150)
	g.legend_.remove()

	plt.title('K-means Clustering with 2 dimensions')
	plt.show()

main()