# SCSE19-0209_Final

Project title: SCSE19-0209 Open source intelligence gathering and data visualisation

Ensure the MongoDB server is started.
Execute python SCSE19-0209_OSIGDV in the command line
Open the browser and navigate to http://127.0.0.1:5000/
The JSON files to merge should be in \SCSE19-0209_Final\scripts\mergeSchema\json_to_merge
The merged JSON file SCSE19_0209.json should be in \SCSE19-0209_Final\scripts\mergeSchema\json_merged

To merge:
Select Merge from the interface.
The JSON files in the folder json_to_merge would appear in a list.
Press the Merge button and wait for a few minutes.
The merged JSON file would be generated in json_merged.

To store:
Select MongoDB from the interface
Select Store from the interface
Press the store button to store SCSE19_0209.json to the MongoDB server

To drop:
The collection SCSE19_0209 should not appear if this is a first installation. Otherwise, the collection may be dropped.
Select MongoDB from the interface
Select Drop from the interface.
Press the drop button to drop SCSE19_0209 from the MongoDB server

To search:
Select MongoDB from the interface.
Select Search from the interface.
Enter the search term and press the search button.
The show search examples button may be pressed to reveal some search terms.

To query:
The collection SCSE19_0209 should be selected.
Find, Distinct, Aggregate or Predefined can be chosen from the dropdown list.

Find:
Find queries can be formed or typed.
The Find examples button may be pressed to reveal some examples.
A JSON file with results is generated.

Distinct:
The distinct query retrieves all the distinct values in a field.
A txt file with results is generated.

Aggregate:
Aggregate queries must be typed.
The Aggregate examples button may be pressed to reveal some examples.
A JSON file with results is generated.

Predefined:
Predefined queries must be selected.
The various options may be selected to modify the predefined query.
Depending on the predefined query selected, the specific term or multiple terms may be selected.
A JSON file with results is generated.

Visualisation:

Singular:
The results from an Aggregate query can displayed by selecting the Singular graph option.
If a search has been made, there will be no need to upload a file.
The parameters must be set and a graph can be generated based on the Aggregate results.

Mutiple:
The results from an Predefined query can displayed by selecting the Mutiple graph option.
If a search has been made, there will be no need to upload a file.
The parameters must be set and a graph can be generated based on the Predefined results.

Clustering and regression options are incomplete and should not be utilised.