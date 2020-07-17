
def w5kParser(filenm):
	prevNonEmpty = True 
	purgePhrases = ["Company Name","Wilshire 5000 Index Membership","Ticker","Page", \
		"As of December 31, 2013"]
	k = []
	v = []
	keyz = False #Our File starts off with values (not keyz)
	with open(filenm) as f: #for reading
		for line in f:
			if (not True in map(lambda x: x in line, purgePhrases)) and \
				(re.match(r'\w',line)):
				#outf.write(re.sub(r'\s+\n','',line.strip(' ')) + "\n")
				if keyz == False:
					v.append(re.sub(r'\s+\n','',line.strip(' ')))
				else:
					k.append(re.sub(r'\s+\n','',line.strip(' ')))
				prevNonEmpty = True
			elif (True in map(lambda x: x in line, purgePhrases)) or \
				(not re.match(r'\w',line)): #IF Purge Word OR Blank line
				if prevNonEmpty == True:
					keyz = not(keyz) #flip the variable
				prevNonEmpty = False

	tks = dict(zip(k,v)) #create the hash from the two list vars
	with open("parsed_"+filenm, 'w') as outf: #outbound file (to be written)
		for key in sorted(tks):
			outf.write('%s\t%s\n' % (tks[key],key))

if __name__ == '__main__':
	import sys, re
	w5kParser(sys.argv[1])


	
	