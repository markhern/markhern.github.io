from bs4 import BeautifulSoup
from urllib.request import urlopen
import re, time

fname = "./state-salaries-db.csv" #output file name
startPg = urlopen("http://data.richmond.com/salaries/2014/state")
startBS = BeautifulSoup(startPg.read(),"html.parser")#or "html.parser" for WIN? | "lxml" 4 linux
agencyList = startBS.findAll("div",{"class":"table-responsive"})[1].find("table",{"class":"table"}).findAll("a",
	{"href":re.compile("^\/salaries\/2014\/state\/")}) #findAll() works here but need findAllNext() 4 empLst 4 some reason?

def empListProc(empList): #pull the emp's individual page
	tmStart = time.time()
	empURL = empList.attrs['href']
	print("empURL = ", empURL)	#DEBUG
	empPg = urlopen("http://data.richmond.com" + empURL)
	eBS = BeautifulSoup(empPg.read(),"html.parser") #or "html.parser" for WIN? | "lxml" 4 linux
	try:
		empName = eBS.find("span",{"id":"personhed"}).getText()
	except AttributeError as aerr:
		try:
			empName = eBS.findAll("h1")[1].find("b").getText() #finds 'Name withheld' type names
		except AttributeError as atErr:
			print("AttributeError for NAME caught; ", str(atErr))
		else:
			if 'Name withheld' in empName:
				empName = '(Name withheld)' #BELOW: Needs clean up for hard returns behind it
	empName = empName[0:empName.find('\n')-1] if '\n' in empName else empName #remove \n
	try: #for some agencies, empWorkLoc is MISSING from page
		empWorkLoc = eBS.find("td",text="Work location").parent()[1].getText()
	except AttributeError:
		empWorkLoc = 'Not Given'
	try: #for some agencies, empHireDt is MISSING from page
		empHireDt = eBS.find("td",text="Hire date").parent()[1].getText()
	except AttributeError:
		empHireDt = 'Not Given'
	empTitle = eBS.find("span",{"id":"personjob"}).getText()
	empPay = eBS.find("h2",{"id":"paytotal"}).getText().replace('$','').replace(',','')
	print(empName,empTitle,empPay,empWorkLoc,empHireDt,"{:.2f}".format(time.time() - tmStart),"secs") #DEBUG
	return (empName,empTitle,empPay,empWorkLoc,empHireDt)

with open(fname, 'w+') as k:

	#Pull each agency's page (and successive pages)
	for agyIdx in range(0,len(agencyList)):
		agyURL = agencyList[agyIdx].attrs['href'] #1st pg of each agency
		agyPager = ''
		while True: #1st & successive Agency pages (employee lists)
			agyPg = urlopen("http://data.richmond.com" + agyURL + agyPager)
			aBS = BeautifulSoup(agyPg.read(),"html.parser")#or "html.parser" for WIN? | "lxml" 4 linux
			agyName = aBS.find("div",{"class":"jumbotron"}).find("div",{"class":"container"}).find("b").getText()
			empLst = aBS.find("tbody",{"id":"name_search"}).findAllNext("a",{"href":re.compile("^\/salaries\/2014\/state\/")})
			print("empLst: ", empLst)	#DEBUG
			for empIdz in range(0,len(empLst)): #each emp on this Agency page
				k.write('"{}","{}","{}","{}","{}","{}"\n'.format(agyName,*empListProc(empLst[empIdz])))
			try:
				urlNxPg = aBS.find("a",text="Next »").attrs['href'] #CHECK THIS
			except AttributeError as atErr:
				print("AttributeError for NEXT PAGE LINK caught; ", str(atErr))
				break #means that this is the last page for this Agency
			else:
				if urlNxPg:
					agyPager = urlNxPg
#				else:
#					break



