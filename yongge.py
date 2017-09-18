import matplotlib

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

labels=[]
with open("/Share/home/zhangqf/liyongge/nmf_for_vivo/ch_cy/onlyp_mbk_labels_for_1000.txt",'rb') as f:
	lines = f.readlines()
	for line in lines:
		each_label = line.replace('\n','')
		labels.append(int(each_label))

change_pattern_unique=[]
with open("/Share/home/zhangqf/liyongge/nmf_for_vivo/ch_cy/onlyp_change_pattern_unique.txt","rb") as f:
	lines = f.readlines()
	for line in lines:
		line = line.replace('\n','')
		each_pattern = line.strip().split(', ')
		float_each_pattern = [float(_s) for _s in each_pattern]
		change_pattern_unique.append(float_each_pattern)

p1=[x for x in range(len(labels)) if labels[x] == 1]
p1_change_pattern_unique=[change_pattern_unique[x] for x in p1]
 
fig = plt.figure()
# plt.plot(p1_change_pattern_unique)
for i in range(10):
	plt.plot(range(20), p1_change_pattern_unique[i],'r')
plt.show()

plt.close()

#plt.savefig('/Share/home/zhangqf/liyongge/nmf_for_vivo/ch_cy/result_picture/onlyp_kmeans_cluster1.png')
