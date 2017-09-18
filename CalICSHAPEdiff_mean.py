import sys

###argv[1] is strucutre nucleotide difference, argv[2] is the stucutre length expect the NULL, argv[3] is the ratio of 
### different nucleotide.
def main():
    files = [ x for x in sys.argv[2:] ]
    for file in files[0:]:
        print calICdiff(file)
def calICdiff(file):
    myfile = open('calICdiff_result', 'w')
    j = 0
    with open(file) as f:
        lines = f.readlines()
        transcriptMap = {}
        formerData = None
        for line in lines[0:]:
            currentData = line.strip().split('\t')
            if formerData != None and currentData[0] == formerData[0]:
                #x = [float(a) if a != 'NULL' else 0.0 for a in formerData[3:]]
                #y = [float(a) if a != 'NULL' else 0.0 for a in currentData[3:]]
                x = []
                y = []
		S = 0
                for index in range(len(formerData[3:])):
			if formerData[index+3] != 'NULL' and currentData[index+3] != 'NULL':
				diff = abs(float(formerData[index+3])-float(currentData[index+3]))
				x.append(float(formerData[index+3]))
				#if diff > float(sys.argv[1]):
				S = S + float(diff)
		myfile.write(str(S) + '\t' + str(len(x)) + '\t')
		#print >>myfile, str(i)+'\t'
		if len(x) == 0:
			continue
		
		#print "ticks" + str(i)

		#if len(x) > float(sys.argv[2]):
		diffration = float(S) / len(x)
		#print diffration
		myfile.write(str(diffration) + '\n')
		#print >>myfile, str(i) + str(diffration) + str(len(x)) + '\t'
		if diffration > float(sys.argv[1]):
			j = j + 1
	    else:
		formerData = currentData
		continue
	    
    f.close()
    return j 
main()
