# To normalize the terms from the health data source
unAuthResultReplacementDict = {"Theft of Resources": ["Theft"]}
actionReplacementDict = {"Physical" : ["Loss","Theft"]}
industryReplacementDict = {tuple(["Medical"]) : ["Healthcare Provider", "Health Plan" , "Healthcare Clearing House", "Business Associate"]}
countryReplacementDict = {"US": "United States","PR" : "PuertoRico", "CN" : "China", "DE" : "Germany", "RU" : "Russian Federation", "RU" : "Russia","CA" : "Canada","GB" : "United Kingdom","LT" : "Lithuania","GU" : "Guam","NZ" : "New Zealand","SE" : "Sweden","AU": "Australia","VE" : "Venezuela","JP" : "Japan","IL" : "Israel","NO" : "Norway","FR" : "France","CH" : "Switzerland","TD" : "Chad", "IN" : "India","ZA" : "South Africa","PL" : "Poland","IE" : "Ireland","BR" : "Brazil","TR" : "Turkey","IR" : "Iran","GY" : "Guyana","ES" : "Spain","PH" : "The Philippines","SA" : "Saudi Arabia","QA" : "Qatar"}