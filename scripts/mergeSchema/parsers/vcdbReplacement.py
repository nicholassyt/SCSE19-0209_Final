# To normalize the terms from the vcdb data source
# Dictionaries allow tuples as keys and there are multiple associations for a single industry
industryReplacementDict = { tuple(["Finance","Bank"]) : ["Commercial Banking" , "Monetary Authorities-Central Bank" , "Investment Banking and Securities Dealing","Offices of Bank Holding Companies","Savings Institutions","Credit Intermediation and Related Activities","Depository Credit Intermediation"],
tuple(["Finance","Real Estate"]) : ["Real Estate","Mortgage and Nonmortgage Loan Brokers","Lessors of Nonresidential Buildings","Lessors of Miniwarehouses and Self-Storage Units","Lessors of Residential Buildings and Dwellings","Rooming and Boarding Houses, Dormitories, and Workers' Camps","Residential Remodelers","New Single-Family Housing Construction","Residential Property Managers"],
tuple(["Finance"]) : ["Securities","Brokerage","Credit Unions","Pension Funds","Other Activities Related to Credit Intermediation","Activities Related to Credit Intermediation","All Other Nondepository Credit Intermediation","Offices of Certified Public Accountants","Tax Preparation Services","Miscellaneous Financial Investment Activities","Investment Advice","Trust, Fiduciary, and Custody Activities","Finance and Insurance","Accounting, Tax Preparation, Bookkeeping, and Payroll Services","Collection Agencies","Financial Transactions Processing, Reserve, and Clearinghouse Activities","Credit Bureaus","Other Financial Investment Activities","Other Accounting Services","Credit Card Issuing","Claims Adjusting","Payroll Services","Consumer Lending","Financial Vehicles","Portfolio Management","Sales Financing","Open-End Investment Funds","Nondepository Credit Intermediation","Commodity Contracts Dealing"],
tuple(["Finance","Insurance"]) : ["Insurance","Reinsurance Carriers"],
tuple(["Medical"]) : ["Hospital","Outpatient","Physicians","Ambulatory","Nursing","Elderly","Pharmacies and Drug Stores","Diagnostic Imaging Centers","Medical, Dental, and Hospital Equipment and Supplies Merchant Wholesalers","Offices of Physical, Occupational and Speech Therapists, and Audiologists","Offices of Dentists","Other Residential Care Facilities","Veterinary Services","Ambulance Services","HMO Medical Centers","Offices of Optometrists","Continuing Care Retirement Communities","Home Health Care Services","Blood and Organ Banks","Health Product Trade","Residential Mental Health and Substance Abuse Facilities","Kidney Dialysis Centers","Offices of Podiatrists","Offices of All Other Miscellaneous Health Practitioners","Health and Welfare Funds","Residential Intellectual and Developmental Disability Facilities","Offices of Chiropractors","Offices of All Other Health Practitioners","Diet and Weight Reducing Centers"],
tuple(["Civil Services"]) : ["Public Finance Activities","Economic","Police Protection","Other General Government Support","Public Administration","Executive, Legislative, and Other General Government Support","Executive and Legislative Offices, Combined","Justice, Public Order, and Safety Activities","Other Justice, Public Order, and Safety Activities","Legal Counsel and Prosecution","International Affairs","Courts","Administration of Education Programs","Administration of Environmental Quality Programs","Fire Protection","Legislative Bodies","Postal Service","Administration of Urban Planning and Community and Rural Development","Administration of Housing Programs, Urban Planning, and Community Development","Parole Offices and Probation Offices","Support Activities for Forestry"],
tuple(["Government"]) : ["Executive Offices","American Indian and Alaska Native Tribal Governments"],
tuple(["Security Services"]) : ["National Security","Correctional Institutions","Security Systems Services","Security Guards and Patrol Services","Investigation Services","Investigation and Security Services"],
tuple(["NGO"]) : ["Environment, Conservation and Wildlife Organizations","Human Rights Organizations","Computer Training","Administration of Conservation Programs"],
tuple(["Social Services"]) : ["Grantmaking","Administration of Public Health Programs","Administration of Veterans' Affairs","Other Individual and Family Services","Educational Support Services","Health Care and Social Assistance","Other Social Advocacy Organizations","Civic and Social Organizations","Administration of Human Resource Programs (except Education, Public Health, and Veterans' Affairs Programs)","Administration of Housing Programs","Child and Youth Services","Social Assistance","Social Advocacy Organizations","Voluntary Health Organizations","Administration of Human Resource Programs","Family Planning Centers","Other Community Housing Services","Vocational Rehabilitation Services"],
tuple(["Associations"]) : ["Business Associations","Professional Organizations","Regulation, Licensing, and Inspection of Miscellaneous Commercial Sectors","Labor Unions and Similar Labor Organizations","Religious, Grantmaking, Civic, Professional, and Similar Organizations"],
tuple(["Legal Services"]) : ["Offices of Lawyers","Court Reporting and Stenotype Services","All Other Legal Services"],
tuple(["Political Organization"]) : ["Political Organizations","Business, Professional, Labor, Political, and Similar Organizations"],
tuple(["Telecommunications"]) : ["Telecommunications","Television Broadcasting","Radio Networks","Radio Stations","Cable and Other Subscription Programming","Telephone Answering Services"],
tuple(["Information Technology"]) : ["Computer","Information","Information Technology Services","Other Personal Services","Software Publishers","Internet Publishing and Broadcasting and Web Search Portals","Data Processing, Hosting, and Related Services","All Other Personal Services","Electronic Shopping and Mail-Order Houses","Other Gambling Industries"],
tuple(["Manufacturing"]) : ["Manufacturing","Mills"],
tuple(["Research"]) : ["Laboratories","Research"],
tuple(["Rental"]) : ["Rental","Lessors of Nonfinancial Intangible Assets"],
tuple(["Advertising"]) : ["Advertising","Other Direct Selling Establishments","Telemarketing Bureaus and Other Contact Centers","Telephone Call Centers"],
tuple(["Consulting Services"]) : ["Consulting Services","Management of Companies and Enterprises","Public Relations Agencies","Office Administrative Services"],
tuple(["Wholesaler"]) : ["Wholesalers","Wholesale Trade","Nursery, Garden Center, and Farm Supply Stores","Linen Supply","All Other Health and Personal Care Stores","Meat Processed from Carcasses","Fruit and Vegetable Canning","Food Service Contractors","Florists"],
tuple(["Food Establishment"]) : ["Food","Beverage","Restaurants","Snack and Nonalcoholic Beverage Bars","Confectionery and Nut Stores","Vending Machine Operators","Cafeterias, Grill Buffets, and Buffets","Drinking Places (Alcoholic Beverages)"],
tuple(["Oil and Gas"]) : ["Oil and Gas Extraction","Gasoline Stations with Convenience Stores","Petroleum","Fossil Fuel Electric Power Generation","Drilling Oil and Gas Wells","Gasoline Stations","Other Gasoline Stations","Petroleum Refineries","Natural Gas Distribution","Support Activities for Oil and Gas Operations"],
tuple(["Retailer"]) : ["Stores","Used Car Dealers","Automobile Dealers","New Car Dealers","Tire Dealers","Recreational Vehicle Dealers","Motor Vehicle and Parts Dealers","Retailers","Home Centers","Retail Trade","Art Dealers"],
tuple(["Utilities"]) : ["Waste","Power Generation","Utilities","Electric Power Distribution","Water Supply and Irrigation Systems","Electric Power Transmission, Control, and Distribution","Wind Electric Power Generation"],
tuple(["Education"]) : ["Schools","Junior Colleges","Child Day Care Services","Educational Services","Flight Training"],
tuple(["Publisher"]) : ["Publishers","Publishing Industries","News Syndicates","Document Preparation Services"],
tuple(["Tourism"]) : ["Travel Agencies","Casinos","Casino Hotels","Hotels (except Casino Hotels) and Motels","Hotels","Motels","Gambling Industries","Amusement and Theme Parks","Other Traveler Accommodation","Amusement, Gambling, and Recreation Industries","All Other Travel Arrangement and Reservation Services","All Other Amusement and Recreation Industries","Tour Operators","Recreational and Vacation Camps","Museums","Traveler Accommodation"],
tuple(["Sport"]) : ["Spectator Sports","Other Spectator Sports","Sports Teams and Clubs","Fitness and Recreational Sports Centers","Sports and Recreation Instruction"],
tuple(["Transport"]) : ["Transportation","Transit","Commuter Rail Systems","Transport","Highway, Street, and Bridge Construction","Limousine Service","General Freight Trucking, Long-Distance, Truckload","Armored Car Services","Taxi Service","General Freight Trucking, Local","Line-Haul Railroads","Parking Lots and Garages","Car Washes"],
tuple(["Airport Operations","Transport"]) : ["Air Traffic Control","Other Airport Operations"],
tuple(["Mining","Metal Industry"]) : ["Mining"],
tuple(["Metal Industry"]) : ["Iron and Steel Forging","Steel Foundries"],
tuple(["Contractors"]) : ["Contractors"],
tuple(["Repair and Maintenance Services"]) : ["Repair"],
tuple(["Engineering Services"]) : ["Engineering Services"],
tuple(["Construction"]) : ["Construction","New Housing For-Sale Builders"],
tuple(["Entertainment"]) : ["Music Publishers","Musical Groups and Artists","Sound Recording Studios","Other Sound Recording Industries","Independent Artists, Writers, and Performers","Motion Picture","Commercial Photography","Arts, Entertainment, and Recreation","Performing Arts","Media Representatives","Agents and Managers for Artists, Athletes, Entertainers, and Other Public Figures"],
tuple(["Delivery Services"]) : ["Specialized Freight","Specialized Freight (except Used Goods) Trucking, Long-Distance","Couriers and Express Delivery Services","Packaging and Labeling Services","Couriers and Messengers","Marine Cargo Handling"],
tuple(["Other Services"]) : ["Translation and Interpretation Services","Other Personal Care Services","Timber Tract Operations","Exterminating and Pest Control Services","Miscellaneous Intermediation","Facilities Support Services","Coin-Operated Laundries and Drycleaners","Beauty Salons","Funeral Homes and Funeral Services","Other Similar Organizations (except Business, Professional, Labor, and Political Organizations)","Other Services (except Public Administration)","Offices of Other Holding Companies"],
tuple(["Printing Services"]) : ["Commercial Printing","Printing"],
tuple(["Agriculture"]) : ["Agriculture","Agricultural","Grape Vineyards","Support Activities for Animal Production"],
tuple(["Event Organizers"]) : ["Convention and Trade Show Organizers","Caterers"],
tuple(["Employment Services"]) : ["Temporary Help Services","Employment Services","Employment Placement Agencies","Professional Employer Organizations","Executive Search Services"],
tuple(["Religious Organization"]) : ["Religious Organizations"],
tuple(["Emergency and Other Relief Services"]) : ["Emergency and Other Relief Services"],
tuple(["Harbour"]) : ["Marinas","Port and Harbor Operations"],
tuple(["Libraries and Archives"]) : ["Libraries and Archives"],
tuple(["Warehousing and Storage"]) : ["Other Warehousing and Storage"],
tuple(["Technical Services"]) : ["Technical Services"],
tuple(["Support Services"]) : ["Support Services"]}

attackerRoleReplacementDict = { "Misuse Trust" : ["Finance","Human resources","End-user","Helpdesk","Manager","System admin","Cashier","Executive","Developer","Customer","Maintenance","Doctor or nurse","Guard","Auditor","Acquaintance","Call center"], "Hackers" : ["Unaffiliated","Activist","Competitor","Former employee","Nation-state","State-affiliated"], "Professional Criminals" : ["Organized crime"]}

attackerRoleRemoveList = ["Organized crime"]

vectorReplacementDict = { tuple(["Backdoor", "C2"]) : ["Backdoor or C2"] , "Email" : ["Email unknown", "Email link", "Email autoexecute", "Email attachment"], "Network" : ["Network propagation"] , "Instant Messaging" : ["IM"]}

vectorRemoveList = ["Backdoor or C2","Email unknown", "Email link", "Email autoexecute", "Email attachment","Network propagation","IM"]

varietyRemoveList = ["Use of backdoor or C2"]

toolReplacementDict = {"Physical Attack" : ["Disabled controls","Hardware Tampering","Tampering","Skimmer","Ram scraper","Surveillance","MitM"],"Script or Program" : ["Download by malware","Backdoor","Downloader","Spyware/Keylogger","Ransomware","Obscuration","Extortion","Password dumper","SSI injection","Packet sniffer","Adminware","Click fraud and cryptocurrency mining","XSS","Session prediction","Session replay","Session fixation","SQLi"],"Information Exchange" : ["C2","Email misuse","Spam","Adware","Misinformation"],"Data Tap" : ["Wiretapping"],"User Command" : ["Command shell","Path traversal","Buffer overflow","Mail command","OS commanding"], "Distributed Tool" : ["Worm"],"ToolKit" : ["Rootkit"]}

vulnerabilityReplacementDict = {"Process" : ["Carelessness","Inadequate processes","Inadequate technology","Inadequate personnel"], "Physical" : ["Documents","Public facility","Partner facility","Uncontrolled location","Partner vehicle","Public vehicle","Partner","Non-corporate","Victim work area","Victim public area","Victim grounds","In-person","Personal residence","Victim secure area","Physical access","Personal vehicle"],
"Design" : ["Web application","Desktop sharing software","Software","Abuse of functionality","Unapproved workaround","Reverse engineering","Programming error"],
"Implementation" : ["Email","SMS","Instant Messaging","Social media","Remote injection","Web download","Exploit vuln","Malfunction","Client-side attack","URL redirector abuse"],
"Configuration" : ["Software update","Phone","Network","VPN","LAN access","Web drive-by","3rd party desktop","Direct install","Website","Remote access","Random error","Desktop sharing","Removable media","Data entry error","Classification error","Misconfiguration","Capacity shortage","Maintenance error","Unapproved hardware","Unapproved software"]}

actionReplacementDict = {"Physical" : ["Carelessness","Loss","Theft","Bribery","Assault","Physical accidents","Omission","Possession abuse","Publishing error","Misdelivery","Data mishandling","Gaffe","Privilege abuse","Disposal error"], "Authenticate" : ["Visitor privileges","Privileged access","Brute force","Use of stolen creds"], "Spoof" : ["Pretexting","Elicitation","Knowledge abuse","Scam","Phishing","Net misuse","Baiting","Influence","Forgery"], "Delete" : ["Destruction","Destroy data"],"Scan" : ["Scan network","Connection"],"Probe" : ["Snooping"], "Flood" : ["DoS","Interruption","Degradation"],"Steal" : ["Capture stored data","Capture app data"],"Copy" : ["Export data"], "Probe" : ["Cryptanalysis","Footprinting"],"Modify" : ["Forced browsing"],"Bypass" : ["Bypassed controls","Disable controls"]}
TVARemoveList = ["RFI","Exploit vuln"]

targetReplacementDict = { "Telephony Services" : ["Telephone","Call center","PBX"], "Financial Devices" : ["Payment switch","Kiosk","PED pad","Gas terminal","POS terminal","POS controller","ATM"], "Device" : ["Fax","Access reader","VoIP adapter","Tablet","Peripheral","Camera","Telemetry","Mobile phone"], "Physical" : ["Former employee","Print","Documents","Payment card","Smart card"], "Account" : ["Partner","System admin","Authentication"], "Process" : ["Web application","DNS"], "Data" : ["Executive","Finance","Manager","End-user","Customer","Directory","Code repository","Human resources","Log","Mail","Database","File","Backup"], "Component" : ["Media","Tapes","Disk media","Flash drive","Disk drive","VM host"], "Computer" : ["Laptop","Desktop","Mainframe"], "Network" : ["WLAN","LAN","Firewall","Router or switch","SAN","Remote access","ICS","Private WAN","Public WAN","IDS"], "Internetwork" : ["Broadband"]}

targetRemoveList = ["Finance","Print","Partner","System admin","Telemetry","VoIP adapter","Former employee","Customer","End-user","Manager","Executive"]

unAuthResultReplacementDict = {"Increased Access" : ["Elevate","Infiltrate","Modify privileges","Created account"], "Disclosure of Information" : ["Exfiltrate","Disclosed","Misrepresentation"], "Corruption of Information" : ["Log tampering","Modify data","Modify configuration","Alter behavior"], "Denial of Service" : ["Defacement"], "Theft of Resources" : ["Fraudulent transaction","Repurpose"]}

unAuthResultRemoveList = ["Hardware tampering","Software installation","Disclosed"]

objectivesReplacementDict = { "Financial Gain" : ["Financial","Asset and fraud","Competitive advantage"], "Political Gain" : ["Espionage"], "Thrill" : ["Fun"], "Damage" : ["Legal and regulatory","Brand damage","Business disruption","Operating costs"], "Status" : ["Fear","Ideology","Grudge"]}

objectivesRemoveList = ["Financial","Secondary","Response and recovery","Operating costs","Opportunistic","Fun"]

malwareReplacementDict = {"CryptoLocker" : ["cryptolocker"], "CryptoWall" : ["cryptowall","Cryptowall"], "Emotet" : ["potentially emotet"]}