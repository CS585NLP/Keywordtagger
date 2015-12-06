#Full model 2

# NN + LDA only 

#!/home/gowthamrang/anaconda/bin


from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import feature
import load
import eval
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
#from sklearn.neural_network import MLPClassifier
#from random import shuffle
import numpy as np
import sys
from sklearn import cross_validation



eval.cleanfile("confusion")
eval.cleanfile("measurement")

class mlp():
	
	def __init__(self,searchmodel=True,keyword_detection_list=None,featurename='bow'):
		self.searchmodel = searchmodel;
		self.documentcount = None;
		self.featurename = featurename;
		self.keyword_detection_list=keyword_detection_list
		self.keywordname = [];
		self.bow = None
	
	

	def train(self,train_target,train_samples):
		self.classifyers={};
		t = len(self.keyword_detection_list)

		self.classes={};
		for each in train_target:
			for x in each:
				self.classes[x] = t;

		self.keywordname = [0]*len(self.keyword_detection_list);
		for i,x in enumerate(self.keyword_detection_list): 
			self.classes[x]=i
		
		self.keyword_detection_list.append('');


		Y = [0]*len(train_samples);
		NewTrain = []
		Ynew = []
		for i,each in enumerate(train_target):
			assert(self.classes[each[0]]<len(self.keyword_detection_list))
			Y[i] = self.classes[each[0]]
			for r in each[1:]:
				Ynew.append(self.classes[r]) 
				NewTrain.append(train_samples[i])
		train_samples.extend(NewTrain); 
		Y.extend(Ynew);
		#print len(self.keyword_detection_list)
		print Y
		#assert(False)

		self.bow = feature.feature(self.featurename,train_samples,keywords=self.keyword_detection_list);
		



		self.clf =  LogisticRegression(solver='lbfgs',warm_start=True,multi_class='multinomial');		
		sets = int(len(train_samples)/10);
		# for each in range(0, len(train_samples),sets):
		# 	X = self.bow.get_incremental_features(train_samples[each:each+sets],Train=True)
		# 	print X.shape, len(Y[each:each+sets])
		# 	self.clf.fit(X,Y[each:each+sets]);
		# 	print 'iteration ... %d' %each
		X = self.bow.get_incremental_features(train_samples,Train=True)
		self.clf.fit(X,Y);

		self.train_target = train_target;		
		self._prepared = True;

	def classify(self,dev_samples):
		
		pred =[]
		assert(self._prepared)
		print 'Hello...in classify'
		X = self.bow.get_incremental_features(dev_samples,Train=False)
		#top tag
		Y = self.clf.predict(X)

		for each in Y.tolist():
			pred.append([]);			
			pred[-1].append(self.keyword_detection_list[each])
		print 'predictions ...', pred
		return pred;



if __name__ == '__main__':

	#A refined form of what we are doing looks so much similar to LDA/PGM.

	print 'Begin Loading samples...'
	train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=10000);
	print 'number of training sample %d'  %len(train_target)
	print 'Tags for the last train example',train_target[-1]
	c=defaultdict(float)
	for each in train_target:
		for everytag in each:
			c[everytag]+=1;
	
	#y = filter(lambda x: c[x]>=500.0 ,c.keys());
	y = c.items()
	y.sort(key = lambda s: -s[1])	#y=['java']
	keywordlist,y = zip(*y);

	y=list(y)[:10]; #first 100 tags only
	print y
	print list(keywordlist)[:10]
	M1 = mlp(True,list(keywordlist)[:10],'bow');
	M1.train(train_target,train_samples);
	import pickle
	pickle.dump(M1,open("full_LR","wb"));
	pickle.dump(list(keywordlist)[:10], open("keyword_lists","wb"))
	
	#eval.evaluate([(M1,u'BOW_NN.csv')],set(list(keywordlist)[:10]));






	


