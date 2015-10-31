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


def Fscore(gold,predicted):
	assert(len(gold) ==len(pred));
	print 'arranging %s test scores',len(gold)
	gold = arrange(gold); 
	predicted = arrange(predicted);
	p,r = precision_recall(gold,predicted);
	
	return (2*p*r)/p+r 



