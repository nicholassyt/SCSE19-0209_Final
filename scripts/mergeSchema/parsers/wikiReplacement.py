# To normalize the terms from the wiki data source
industryReplacementDict = {
    tuple(["Medical"]) : ["healthcare"],
	tuple(["Information Technology"]) : ["tech" , "tech, web", "tech, retail", "gaming", "social network", "web, gaming", "local search", "web, military"],
	tuple(["Transport"]) : ["transport"],
	tuple(["Finance"]) : ["financial", "consulting, accounting", "financial, credit reporting", "financial service company"],
	tuple(["Finance","Bank"]) : ["banking"],
	tuple(["Retailer"]) : ["retail", "fashion", "Consumer Goods"],
	tuple(["Telecommunications"]) : ["telecoms", "telecommunications"],
	tuple(["Government"]) : ["government","political", "government, healthcare", "government, database", "military, healthcare", "government, military"],
	tuple(["Utilities"]) : ["energy"],
	tuple(["Food Establishment"]) : ["restaurant"],
	tuple(["Tourism"]) : ["hotels"],
	tuple(["Education"]) : ["academic"],
	tuple(["Research"]) : ["genealogy", "Clinical Laboratory"],
	tuple(["Other Services"]) : ["Question & Answer"],
	tuple(["Entertainment"]) : ["media", "arts group"],
	tuple(["Security Services"]) : ["military"],
	tuple(["Advertising"]) : ["ticket distribution", "Telephone directory"]}