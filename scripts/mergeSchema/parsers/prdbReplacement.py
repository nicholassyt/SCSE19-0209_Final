# To normalize the terms from the prdb data source
vulnerabilityReplacementDict = {"Process" : ["Carelessness","Inadequate processes","Inadequate technology","Inadequate personnel"], "Physical" : ["Documents","Public facility","Partner facility","Uncontrolled location","Partner vehicle","Public vehicle","Partner","Non-corporate","Victim work area","Victim public area","Victim grounds","In-person","Personal residence","Victim secure area","Physical access","Personal vehicle"],
"Design" : ["Web application","Desktop sharing software","Software","Abuse of functionality","Unapproved workaround","Reverse engineering","Programming error"],
"Implementation" : ["Email","SMS","Instant Messaging","Social media","Remote injection","Web download","Exploit vuln","Malfunction","Client-side attack","URL redirector abuse"],
"Configuration" : ["Software update","Phone","Network","VPN","LAN access","Web drive-by","3rd party desktop","Direct install","Website","Remote access","Random error","Desktop sharing","Removable media","Data entry error","Classification error","Misconfiguration","Capacity shortage","Maintenance error","Unapproved hardware","Unapproved software"]}

actionReplacementDict = {"Physical" : ["Carelessness","Loss","Theft","Bribery","Assault","Physical accidents","Omission","Possession abuse","Publishing error","Misdelivery","Data mishandling","Gaffe","Privilege abuse","Disposal error"], "Authenticate" : ["Visitor privileges","Privileged access","Brute force","Use of stolen creds"], "Spoof" : ["Pretexting","Elicitation","Knowledge abuse","Scam","Phishing","Net misuse","Baiting","Influence","Forgery"], "Delete" : ["Destruction","Destroy data"],"Scan" : ["Scan network","Connection"],"Probe" : ["Snooping"], "Flood" : ["DoS","Interruption","Degradation"],"Steal" : ["Capture stored data","Capture app data"],"Copy" : ["Export data"], "Probe" : ["Cryptanalysis","Footprinting"],"Modify" : ["Forced browsing"],"Bypass" : ["Bypassed controls","Disable controls"]}

toolReplacementDict = {"Physical Attack" : ["Disabled controls","Hardware Tampering","Tampering","Skimmer","Ram scraper","Surveillance","MitM"],"Script or Program" : ["Download by malware","Backdoor","Downloader","Spyware/Keylogger","Ransomware","Obscuration","Extortion","Password dumper","SSI injection","Packet sniffer","Adminware","Click fraud and cryptocurrency mining","XSS","Session prediction","Session replay","Session fixation","SQLi"],"Information Exchange" : ["C2","Email misuse","Spam","Adware","Misinformation"],"Data Tap" : ["Wiretapping"],"User Command" : ["Command shell","Path traversal","Buffer overflow","Mail command","OS commanding"], "Distributed Tool" : ["Worm"],"ToolKit" : ["Rootkit"]}

TVARemoveList = ["RFI","Exploit vuln"]

vectorList = ['Malware','Network','Personal vehicle', 'Web application', 'Phone', 'Victim work area', 'Email', 'SMS', 'Web drive-by', 'Victim public area', 'Victim grounds', 'In-person', 
				'Backdoor or C2', 'Personal residence', 'Victim secure area', 'Privileged access', 'Website', 'Public facility', 'Direct install', 'Software', 'Partner facility', 
				'Desktop sharing', 'Desktop sharing software', 'Documents', 'Uncontrolled location', 'Social media', 'Partner vehicle', 'Command shell', 'Remote injection', '3rd party desktop', 'Web download', 
				'Partner', 'Download by malware', 'Physical access', 'Public vehicle', 'Software update', 'Removable media', 'VPN', 'Network propagation', 'Visitor privileges']
				
varietyDict = { "HACK" : "Hack", "INSD" : "Insider", "CARD" : "Payment Card", "PHYS": "Physical Loss", "PORT" : "Portable Device", "STAT" : "Stationery Device", "DISC" : "Unintended Disclosure"}

varietyList = ['Loss', 'Theft', 'Exploit vuln', 'Misdelivery', 'Brute force', 'Data mishandling', 'Gaffe', 'Pretexting', 'Knowledge abuse', 'Destruction', 'Disabled controls', 'Tampering', 
				'Privilege abuse', 'Backdoor', 'C2', 'Phishing', 'Scan network', 'Use of stolen creds', 'Disposal error', 'DoS', 'Interruption', 'Publishing error', 'Possession abuse', 
				'Skimmer', 'Malfunction', 'XSS', 'Ram scraper', 'Misconfiguration', 'Bribery', 'Capture stored data', 'Downloader', 'Export data', 'Spyware/Keylogger', 'Use of backdoor or C2', 
				'SQLi', 'Ransomware', 'Programming error', 'Capture app data', 'Bypassed controls', 'Obscuration', 'Disable controls', 'Rootkit', 'Surveillance', 'Net misuse', 'Extortion', 'Path traversal', 
				'Baiting', 'Influence', 'Destroy data', 'Degradation', 'Client-side attack', 'Forgery', 'Abuse of functionality', 'Email misuse', 'Propaganda', 'Illicit content', 'Assault', 'Elicitation', 
				'Wiretapping', 'Password dumper', 'Unapproved hardware', 'Reverse engineering', 'Spam', 'Scam', 'Snooping', 'MitM', 'URL redirector abuse', 'Classification error', 'Adware', 
				'Forced browsing', 'Misinformation', 'Worm', 'Click fraud and cryptocurrency mining', 'Physical accidents', 'Unapproved workaround', 'Data entry error', 'SSI injection', 'Buffer overflow', 
				'Omission', 'Packet sniffer', 'Adminware', 'RFI', 'Unapproved software', 'Cryptanalysis', 'Mail command injection', 'Footprinting', 'Maintenance error', 'Capacity shortage', 'Session fixation', 
				'OS commanding', 'Session prediction', 'Session replay']

industryReplacementDict = { "MED" : "Medical", "EDU" : "Education", "BSF" : "Finance" , "GOV" : "Government" , "BSR" : "Retailer"}