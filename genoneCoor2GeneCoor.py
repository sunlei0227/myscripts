#!/Share/home/zhangqf/usr/anaconda/bin/python

##usage python ~/sunlei/sw/myscript/genoneCoor2GeneCoor.py ~/sunlei/data/human/human.gene.bed input_file[ex./Share/home/zhangqf/sunlei/data/RBP/human2/forxukui/forxukui_hg38/ADAR_CLIP_hg38.bed] output_file
import sys


geneCoor = sys.argv[1]
bedSite = sys.argv[2]
output = sys.argv[3]

#ensemblesite = open(output, 'w')
d = dict()
gene = []
with open(geneCoor, 'r') as f:
	lines = f.readlines()
	for line in lines:
		genesite = line.strip().split("\t")
		genesite[0] = "chr"+genesite[0]
		if genesite[0] in d.keys():
			d[genesite[0]].append([genesite[1],genesite[2],genesite[3],genesite[4],genesite[5]])
		else:
			d[genesite[0]] = []
			d[genesite[0]].append([genesite[1],genesite[2],genesite[3],genesite[4],genesite[5]])
				
#		d[genesit] = [genesite[0],genesite[1],genesite[2],genesite[4],genesite[5]]
#		print "==",d
#		gene.append(d)
#print "===d==",d[0],d[0][0],d[0][1],"===",d[1]
#print d[genesite[1]],genesite[3],genesite[2]


#k_list = sorted(d.keys())
#for k in d.keys():
#	print "===11==",d[k]
OUTPUT = open(output,'w')
mydata = []
partial = []
binding = []
#d1 = dict()
s = 0
i = 1
with open(bedSite, 'r') as f:
        lines = f.readlines()
        for line in lines:
		bindingsite = line.strip().split("\t")
		if bindingsite[0] in d.keys():
			for gene in d[bindingsite[0]]:
				if int(bindingsite[2]) <= int(gene[0]):
					continue
				elif int(bindingsite[1]) >= int(gene[1]):
					continue
				elif int(bindingsite[1]) >= int(gene[0]) and int(bindingsite[2]) <= int(gene[1]):
					if gene[4] == "+":
						absstar = int(bindingsite[1]) - int(gene[0])
   	                                        absend = int(bindingsite[2]) - int(gene[0])
#						mydata.append([bindingsite,str(gene[2]),str(absstar),str(absend)])
						print >> OUTPUT,bindingsite[0]+"\t"+bindingsite[1]+"\t"+bindingsite[2]+"\t"+bindingsite[3]+"\t"+bindingsite[4]+"\t"+bindingsite[5]+"\t"+bindingsite[1]+"\t"+bindingsite[2]+"\t"+str(gene[2])+"\t"+str(absstar)+"\t"+str(absend)
						s += i
						i += 1
					else:
						absstar = int(gene[1]) - int(bindingsite[2])
                                	        absend = int(gene[1]) - int(bindingsite[1])
#						mydata.append([bindingsite,str(gene[2]),str(absstar),str(absend)])
						print >> OUTPUT, '\t'.join(bindingsite)+"\t"+bindingsite[1]+"\t"+bindingsite[2]+"\t"+str(gene[2])+"\t"+str(absstar)+"\t"+str(absend)
						s += i
						i +=1
				else:
					partial.append(bindingsite)
		else:
			continue
#print "===sl=="+str(mydata)+str(i)			
#		d1 = [bindingsite[0],bindingsite[1],bindingsite[2],bindingsite[3],bindingsite[4],bindingsite[5]]
#		binding.append(d1)
#print binding,len(binding)

#print genesite[1],genesite[2]
'''i = 0 
mydata = []
for i in range(len(binding)):
	d1[i][1]>=d[d1[i][0]]
	print "=====binding===="+binding[i][0]
	for k in d.keys():
#		print "=====gene==="+d[k][0]
#		if d[k][0] == binding[i][0]:
#			mydata = []
		if binding[i][1]>=d[k][1] and binding[2]<=d[k][2]:
#				print binding[i][1],binding[i][2],d[k][1],d[k][2]
				if d[k][3] == "+":
					absstar = int(binding[i][1]) - int(d[k][1])
					absend = int(binding[i][2]) - int(d[k][1]) 
					mydata.append(binding[i],binding[i][1],binding[i][2],k,str(absstar),str(absend))
#				if d[k][3] == "-":
				else:
					absstar = int(d[k][2]) - int(binding[i][2])
					absend = int(d[k][2]) - int(binding[i][1])
					mydata.append(binding[i],binding[i][1],binding[i][2],k,str(absstar),str(absend))
		else:
			continue
print mydata'''
#else:
#	continue
#output = open(output,'w') 

#print >>output, ' '.join(str(mydata))
