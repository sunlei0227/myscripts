
import sys                                                                                                                                                                                                                                    
         

input =sys.argv[1]
#output = open(sys.argv[2].'w')
print input
d ={}    
lncRNA =0
miRNA =0 
misc_RNA =0
other =0 
protein_coding =0
pseudogene =0
rRNA =0   
snoRNA =0 
snRNA =0 
with open(input,'r') as f:
    line= f.readline()
    while line:
        arr = line.strip().split()
        d[arr[1]] = arr[4:]
#       line = f.readline()
        if arr[1] =="lncRNA":
            for i in arr[4:]:
                if i != "NULL":
                    lncRNA +=1
                else:
                    continue
        if arr[1] =="miRNA":     
            for i in arr[4:]:
                if i != "NULL":
                    miRNA +=1
                else:        
                    continue
        if arr[1] =="misc_RNA":
            for i in arr[4:]:   
                if i != "NULL":
                    misc_RNA +=1
                else:        
                    continue
        if arr[1] =="other":
            for i in arr[4:]:   
                if i != "NULL":
                    other +=1
                else:        
                    continue
        if arr[1] =="protein_coding":
            for i in arr[4:]:   
                if i != "NULL":
                    protein_coding +=1
                else:        
                    continue
        if arr[1] =="pseudogene":
            for i in arr[4:]:   
                if i != "NULL":
                    pseudogene +=1
                else:        
                    continue
        if arr[1] =="rRNA":
            for i in arr[4:]:   
                if i != "NULL":
                    rRNA +=1
                else:
					continue
        if arr[1] =="snoRNA":
            for i in arr[4:]:
                if i != "NULL":
                    snoRNA +=1
                else:
                    continue
        if arr[1] =="snRNA":
            for i in arr[4:]:
                if i != "NULL":
                    snRNA +=1
                else:
                    continue
	line = f.readline()
print 'protein_coding '+ str(protein_coding)+'\n'+'lncRNA '+str(lncRNA)+'\n'+'pseudogene '+str(pseudogene) +'\n'+'misc_RNA '+str(misc_RNA)+'\n'+ 'miRNA '+str(miRNA)+'\n'+'snRNA '+str(snRNA) +'\n'+'snoRNA '+str(snoRNA)+'\n'+'rRNA '+str(rRNA)
