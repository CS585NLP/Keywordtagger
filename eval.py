#Evaluation metric

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
    tp=0
    fp=0
    tn=0
    fn=0
    for exampleno,each in enumerate(pred):
        if each>0 and gold[exampleno]>0 :
            tp+=1
        elif each>0  and gold[exampleno]==0 :
            fp+=1
        elif  each==0  and gold[exampleno]==0 :
            tn+=1
        else:
            fn+=1

    print "precision is "+str(tp*1.0/(tp+fp))
    print "recall is "+str(tp*1.0/(tp+fn))
    print "accuracy is "+str((tp+tn)*1.0/(tp+fp+fn+tn))

def Fscore(gold,predicted):
	assert(len(gold) ==len(pred));
	print 'arranging %s test scores',len(gold)
	gold = arrange(gold); 
	predicted = arrange(predicted);
	p,r = precision_recall(gold,predicted);
	
	return (2*p*r)/p+r 



