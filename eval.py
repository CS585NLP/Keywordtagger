def cleanfile(fname):
	f = open(fname,'w');
	f.close();


def writeintofile(x,fname):
	f = open(fname,'a');
	f.write(x+'\n')
	f.close();

#Evaluation metric
def confused_examples(target,sample,gold,pred, number):
	type1=[]
	type2=[]
	for exno,[x,y] in enumerate(zip(gold,pred)):
		if(x==1 and y==0 and len(type1)<number):
			type1.append(exno);
		if(x==0 and y==1 and len(type2)<number):
			type2.append(exno);
		if(len(type2)>=3 and len(type1)>=3):
			break;
	x='';
	x+='Examples are positive but classified incorrectly'
	for each in type1: x += str(sample[each])+'\n'#+target[each]
	x+='Examples are negative but classifyed incorrectly'+'\n'
	for each in type2: x += str(sample[each])+'\n'#+target[each]
	writeintofile(x,"confusion");

def arrange(x):
	y=[];
	for each in x:
		y.append(set(each));
	return y;

def precision_recall(gold,pred):
	n,d1,d2=[0.0]*3;
	for x,y in zip(gold,pred):
		n+=len(x.intersection(y))
		d1+= len(y);
		d2+=len(x)
	return n//d1,n//d2;

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



