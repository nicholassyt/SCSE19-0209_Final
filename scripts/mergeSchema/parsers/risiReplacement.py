# To normalize the terms from the risi data source
industryReplacementDict = {
	tuple(["Manufacturing"]) : ["Chemical","Pharmaceutical","Electronic Manufacturing","General Manufacturing","Automotive","Pulp and Paper"],
	tuple(["Oil and Gas"]) : ["Petroleum"],
	tuple(["Utilities"]) : ["Power and Utilities","Water/Waste Water"],
	tuple(["Food and Beverage"]) : ["Food Establishment"],
	tuple(["Other Services"]) : ["Other"],
	tuple(["Mining","Metal Industry"]) : ["Mining"],
	tuple(["Metal Industry"]) : ["Metals"]}

countryReplacementDict = {"US": "United States","PR" : "PuertoRico", "CN" : "China", "DE" : "Germany", "RU" : "Russian Federation", "CA" : "Canada","GB" : "United Kingdom","LT" : "Lithuania","GU" : "Guam","NZ" : "New Zealand","SE" : "Sweden","AU": "Australia","VE" : "Venezuela","JP" : "Japan","IL" : "Israel","NO" : "Norway","FR" : "France","CH" : "Switzerland","TD" : "Chad", "IN" : "India","ZA" : "South Africa","PL" : "Poland","IE" : "Ireland","BR" : "Brazil","TR" : "Turkey","IR" : "Iran","GY" : "Guyana","ES" : "Spain","PH" : "The Philippines","SA" : "Saudi Arabia","QA" : "Qatar", "IT" : "Italy", "EU" : "Europe", None : "Unknown"}