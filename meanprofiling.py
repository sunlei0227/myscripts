import sys

vitro = []
vivo = []
with open(sys.argv[1],'r') as f:
	line = f.readline()
	while line:
		arr = line.strip().split()
		vitro.append(arr[1].split(','))
		vivo.append(arr[2].split(','))
#		print vitro, vivo
		line =f.readline()
#print vivo
def meanicshapeprofiling(vivo):
#vivo is a list
	vivoprofiling = []
	sum = 0
	for j in range(len(vivo[1])):
		for i in range(len(vivo)):
			if i == len(vivo)-1:
				vivoprofiling.append(sum/int(len(vivo)))
				sum = 0
			else:
				sum += float(vivo[i][j])
	return vivoprofiling

print "vivo profiling"+'\n' + str(meanicshapeprofiling(vivo))
print "vitro profiling" + '\n' + str(meanicshapeprofiling(vitro))
