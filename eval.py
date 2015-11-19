import load 
import csv


def cleanfile(fname):
	f = open(fname,'w');
	f.close();


def writeintofile(x,fname):
	f = open(fname,'a');
	f.write(x+'\n')
	f.close();

#Evaluation metric
def confused_examples(classname,target,sample,gold,pred, number):
	type1=[]
	type2=[]
	for exno,[x,y] in enumerate(zip(gold,pred)):
		if(x==1 and y==0 and len(type1)<number):
			type1.append(exno);
		if(x==0 and y==1 and len(type2)<number):
			type2.append(exno);
		if(len(type2)>=3 and len(type1)>=3):
			break;
	x='Confusion for class '+classname+'\n';
	x+='Examples are positive but classified incorrectly\n'
	for each in type1: x += str(sample[each])+'\n'#+target[each]
	x+='Examples are negative but classifyed incorrectly\n'
	for each in type2: x += str(sample[each])+'\n'#+target[each]
	writeintofile(x,"confusion");

def precision_recall_per_class(gold, pred):
	tp,fp,fn,tn = [0.0]*4;
	for p,q in zip(gold,pred):
		tp += (p==1 and q==1);
		fp += (p==1 and q==0);
		fn += (p==0 and q==1);
		tn += (p==0 and q==0);
		
	return [tp/(tp+fp+0.1), tp/(tp+fn+0.1),(tp+tn)/(tp+fp+tn+fn),tp,tn,fp,fn]

    # tp=0
    # fp=0
    # tn=0
    # fn=0    
    # for exampleno,each in enumerate(pred):
    #     if each==1 and gold[exampleno]==1 :
    #         tp+=1
    #     elif each==1  and gold[exampleno]==0 :
    #         fp+=1
    #     elif  each==0  and gold[exampleno]==0 :
    #         tn+=1
    #     else:
    #         fn+=1
    
    # print "precision is "+str(tp*1.0/(tp+fp+0.0000001))
    # print "recall is "+str(tp*1.0/(tp+fn+0.00000001))
    # print "accuracy is "+str((tp+tn)*1.0/(tp+fp+fn+tn+0.0000001))

def Fscore(gold,predicted):
	assert(len(gold) ==len(pred));
	print 'arranging %s test scores',len(gold)
	gold = arrange(gold); 
	predicted = arrange(predicted);
	p,r = precision_recall(gold,predicted);
	
	return (2*p*r)/p+r 


#evaluate 
def evaluate(models,classes):
	models, fname = zip(*models);
	fname=fname[0]

	print 'Loading Test dataset...'
	dev_samples,gold = load.load_dataset(fname=load.filename['TEST'],numdocs=1000);
	[tp,fp,fn,tn] = [0.0,0.0,0.0,0.0]
	keyword_stats=[]
	confusion=[]
	for each in models:
		confusion.append({e:[[],[]] for e in classes})
		keyword_stats.append({e:[0.0,0.0,len(dev_samples)*1.0,0.0] for e in classes});
		print 'Evaluation Cache for %s is not present' %fname
		pred = each.classify(dev_samples); #a sorted vector of strings
		assert(len(pred) ==len(dev_samples));		
		for no,each in enumerate(pred):
			print '\rVerifying output for example %d' %no,
			assert(type(each) == list);
			p=set(each)&classes; 
			q=set(gold[no])&classes;
			r = p&q;
			tp += len(p&q);
			tn += len(classes)-len(p|q);
			fp += len(p)-len(p&q)
			fn += len(q)-len(p&q)		


			for every in r: keyword_stats[-1][every][0]+=1; #tp
			for every in p-r: keyword_stats[-1][every][1]+=1; #fp
			for every in p|q: keyword_stats[-1][every][2]-=1; #tn
			for every in q-r: keyword_stats[-1][every][3]+=1; #fn

			#for every in r: confusion[-1][every][0].append(exampleno); #tp
			for every in p-r: confusion[-1][every][0].append(no); #fp
			#for every in p|q: keyword_stats[-1][every][2].append(exampleno); #tn
			for every in q-r: confusion[-1][every][1].append(no); #fn

		#write into file	
		#print keyword_stats[-1]
		#print [tp,tn,fp,fn]

		with open(fname, 'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=list(classes))	     
			writer.writeheader()
			for each in keyword_stats:
				writer.writerow(each)
    	prec,rec = tp/(tp+fp+0.01),tp/(tp+fn+0.01)
    	#print prec,rec
    	print '\n'
    	print '[tp,fp,tn,fn]',keyword_stats[-1]
    	print '------tp------tn------fp------fn------pr-------re------f1------'
    	print '----------------------------Model %s--------------------------' %fname
    	print '------%d------%d------%d------%d------%.2f------%.2f------%.2f------' %(tp,tn,fp,fn,prec,rec,2*prec*rec/(prec+rec+0.01))
    	x= '%s \n' %confusion[-1]
    	for each in confusion[-1]:
    		x+= 'confusion in %s \n' %each    		
    		for no in confusion[-1][each]:     			
    			for examp in  no[:3]:
    				x+= '%s \n' %examp
    				x+= '%s %s\n' %(dev_samples[examp],gold[examp])
    		x+= '---------------------------------\n'
		writeintofile(x,"confusion")



cleanfile("confusion")
cleanfile("measurement")
