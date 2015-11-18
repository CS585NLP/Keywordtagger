#Full model
#Search [to exploit sparseness] + LR-classifier
#N

#!/home/gowthamrang/anaconda/bin

#NBClassifier with BOW model max likelhood training

from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import feature
import load
import eval
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
#from random import shuffle
import numpy as np
import sys
from sklearn import cross_validation



eval.cleanfile("confusion")
eval.cleanfile("measurement")

class search_classify():
	
	def __init__(self,searchmodel=True,keyword_detection_list=None,featurename='bow_bigram'):
		self.searchmodel = searchmodel;
		self.documentcount = None;
		self.featurename = featurename;
		self.keyword_detection_list=keyword_detection_list
		self.bow = None
		#print self.keyword_detection_list
		print 'Model :- tfidf for search space reduction then (LR features) classification'
 
	def train(self,train_target,train_samples):
		self._prepared = False;
		self.tfidf = TfidfVectorizer(stop_words='english')		
		self.tfidf.fit_transform(train_samples[1]+train_samples[2]); #title and description
		#Classifier Model
		self.classifyers={};
		classes=[];
		if not self.keyword_detection_list :
			for each in train_target: classes.extend(x for x in each);		
			classes = set(classes);
		else:
			classes = self.keyword_detection_list;

		print 'Total number of classes for this model ', len(classes)
		class_example_count = []
		for each in classes:
		  Y =[1 if each in x  else 0 for x in train_target ];
		  class_example_count.append(sum(Y));		
		print 'examples seen for each class during training ' ,class_example_count

		self.bow = feature.feature(self.featurename,train_samples,keywords=self.keyword_detection_list);
		metric = []; 
		#Classifier Model : Train
		for each in classes:  
			#Balancing dataset
			target_y = [1 if each in x  else 0 for x in train_target ];
			[target_y_balanced, train_balanced]=load.split_equally(target_y,train_samples)
			#[target_y_balanced, train_balanced] = [target_y,train_samples]
			#print 'Not balancing test/train'
			print 'Training to tag %s from %d samples' %(each ,len(target_y_balanced))
			Y =np.array(target_y_balanced);

			X = self.bow.get_incremental_features(train_balanced);
			assert(X.shape[0] ==  len(train_balanced))
			assert(Y.shape[0] == len(train_balanced))

			#if not LOGISTIC_REGRESSION:
			#	clf = MultinomialNB(fit_prior=False);# onlu MultinomialNB takes sparse matrix , to offset hughe neg samples
			#else:
			clf = LogisticRegression();

			clf.fit(X,Y);
			#pred = cross_validation.cross_val_predict(clf, X , Y, cv=3);
			self.classifyers[each] = clf;  
			#eval.confused_examples(each,train_target,train_balanced,Y.tolist(),pred,3)
			#metric.append((each,prec,rec,acc,tp,tn,fp,fn))
		self.train_target = train_target;
		x = [eachtraindoc[1] for eachtraindoc in train_samples]
		print 'tfidf ..'
		self.tfidfVec = self.tfidf.fit_transform(x);
		self.tfidfVec = self.tfidfVec.transpose();
		print self.tfidfVec.shape
		self._prepared = True;

	def classify(self,dev_samples):
		
		pred =[]
		assert(self._prepared)
		print 'Hello...in classify'
		X = self.bow.get_incremental_features(dev_samples,Train=False)

		for dev_no,each in enumerate(dev_samples):
			pred.append([]);
			result=[]
			#print each[1]
			response = self.tfidf.transform([each[1]]);#title+description
			v = response.dot(self.tfidfVec);	
			#print v.get_shape()
			v = v.toarray();
			v= v.tolist();
			#print v[0][20]
			for no,val in enumerate(v[0]):				
				if(val>0.01): result.append((val,no))	
			
			#top 10 docs with similarity
			#print result[:20]

			result = sorted(result,key=lambda x: -x[0])
			result =result[:10];
			
			testclassifiers=[]
			for _,docno in result: testclassifiers.extend(self.train_target[docno])
			testclassifiers = set(testclassifiers);
			#print '\rtesting with classifiers', testclassifiers;
			for everyclassifyer in testclassifiers:
				if everyclassifyer in self.keyword_detection_list:
					if self.classifyers[everyclassifyer].predict(X.getrow(dev_no)):
						pred[-1].append(everyclassifyer);
					
			#print 'Tags for this one', pred
			#assert(False)
		print pred
		return pred;



if __name__ == '__main__':

	#A refined form of what we are doing looks so much similar to LDA/PGM.
	#Deep learning to learn feature end-end is better

	print 'Begin Loading samples...'
	train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=None);
	print 'number of training sample %d'  %len(train_target)
	print 'Tags for the last train example',train_target[-1]
	c=defaultdict(float)
	for each in train_target:
		for everytag in each:
			c[everytag]+=1;
	
	y = filter(lambda x: c[x]>=500.0 ,c.keys());
#y=['java']
	print y
	
	M1 = search_classify(True,y,'bow_bigram');
	M1.train(train_target,train_samples);
	eval.evaluate([(M1,u'tfidf_LR.csv')],set(M1.classifyers.keys()));

	#eval.confused_examples(classname,target,sample,gold,pred, number):






	


