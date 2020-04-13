import os

#File path constants
JSONEXT = ".json"
JSONToMergeFolder = os.path.join(os.path.dirname(__file__), "json_to_merge/")
JSONMergedFolder = os.path.join(os.path.dirname(__file__), "json_merged/")

# Type constants
prdbType = "prdb"
vcdbType = "vcdb"
nvdcveType = "nvdcve"
healthType = "health"
risiType = "risi"
wikiType = "wiki"
#exampleType = "example"
nullValue = None

#JSON files
prdbFileName = JSONToMergeFolder + prdbType + JSONEXT
vcdbFileName = JSONToMergeFolder + vcdbType + JSONEXT
healthFileName = JSONToMergeFolder + healthType + JSONEXT
risiFileName = JSONToMergeFolder + risiType + JSONEXT
wikiFileName = JSONToMergeFolder + wikiType + JSONEXT
JSONMergedFileName = JSONMergedFolder + "SCSE19_0209" + JSONEXT
#nvdcveFileName = JSONToMergeFolder  + nvdcveType + JSONEXT
#exampleFileName = JSONToMergeFolder  + exampleType + JSONEXT

# Fields of schema defined in a dictionary
fieldsToAdd = {"typeId" : nullValue, "incident_date" : { "date" : nullValue, "year" : nullValue, "month" : nullValue, "day" : nullValue, "isEstimate" : nullValue},
				"resolution_date" : { "date" : nullValue, "year" : nullValue, "month" : nullValue, "day" : nullValue, "resolution_value" : nullValue,"resolution_unit": nullValue},
				"notification_date" : { "date" : nullValue, "year" : nullValue, "month" : nullValue, "day" : nullValue, "isEstimate" : nullValue},
				"entry_date": { "date" : nullValue, "year" : nullValue, "month" : nullValue, "day" : nullValue},
				"victim" : nullValue, "industry" : nullValue, "country" : nullValue, "state" : nullValue, "employee_count" : nullValue,
				"attacker" : {"name" : nullValue, "origin" : nullValue, "role" : nullValue},"objectives" : nullValue, "discovered_by" : nullValue,
				"cve" : nullValue, "malware_used" : nullValue, "tool" : nullValue, "vulnerability" : nullValue, "action" : nullValue,
				"target" : {"targeted" : nullValue, "records_affected" : nullValue, "assets_affected" : nullValue},
				"unauthorized_result" : nullValue,
				"monetary_loss" : {"original_currency" : nullValue,"unconverted" : nullValue,"currency" : nullValue, "amount" : nullValue,"isEstimate": nullValue},
				"description" : nullValue, "info_source" : nullValue, "source_link" : nullValue}

#Rates for conversion to USD if there is no available value in the CurrencyConverter Library 
ratesAgainstUSD = {"GBP" : 1.22, "EUR" : 1.10, "ZAR" : 0.065, "INR" : 0.014, "THB" : 0.033, "KRW" : 0.00083, "CAD" : 0.75, "AUD" : 0.67, "CZK" : 0.043}		