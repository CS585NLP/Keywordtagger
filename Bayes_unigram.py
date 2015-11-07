#!/home/gowthamrang/anaconda/bin

#NBClassifier with BOW model max likelhood training

from __future__ import division

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

LOGISTIC_REGRESSION=False
if len(sys.argv)>1:
  if('L' in sys.argv[1:]):
    LOGISTIC_REGRESSION = True;

if LOGISTIC_REGRESSION:
  print 'LogisticRegression is Active';
else:
  print 'NB is Active';

print 'Begin Loading samples...'
train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=None);
#dev_samples,dev_target = load.load_dataset(fname=load.filename['DEV'],numdocs=None);
print 'number of training sample %d'  %len(train_target)
print 'Tags for the last train example',train_target[-1]

#Classifier Model
classifyers=[];
classes=[];
for each in train_target: classes.extend(x for x in each);
classes = set(classes);
print 'Total number of classes for this model ', len(classes)

class_example_count = []
for each in classes:  
  Y =[1 if each in x  else 0 for x in train_target ];
  class_example_count.append(sum(Y));
assert(sum(class_example_count) == len(train_target))
print 'examples seen for each class during training ' ,class_example_count

classes=['python']
#Feature Model
if not LOGISTIC_REGRESSION:
    bow = feature.feature("bow",train_samples);
else:
    bow_trimmed = feature.feature("bow_bigram",train_samples);

metric = []; 
#Classifier Model : Train
for each in classes:  
  #Balancing dataset
  target_y = [1 if each in x  else 0 for x in train_target ];
  [target_y_balanced, train_balanced]=load.split_equally(target_y,train_samples)
  print 'Training to tag %s from %d samples' %(each ,len(target_y_balanced))
  Y =np.array(target_y_balanced);

  if not LOGISTIC_REGRESSION:   
   X = bow.get_incremental_features(train_balanced);
  else:  
   X = bow_trimmed.get_incremental_features(train_balanced);
  assert(X.shape[0] ==  len(train_balanced))
  assert(Y.shape[0] == len(train_balanced))
  if not LOGISTIC_REGRESSION:
    clf = MultinomialNB(fit_prior=False);# onlu MultinomialNB takes sparse matrix , to offset hughe neg samples
  else:
    clf = LogisticRegression();
  #clf.fit(X,Y);
  pred = cross_validation.cross_val_predict(clf, X , Y, cv=3);
  [prec,rec,acc,tp,tn,fp,fn] = eval.precision_recall_per_class(Y.tolist(),pred)  
  #classifyers.append(clf);  
  eval.confused_examples(train_target,train_balanced,Y.tolist(),pred,3)
  metric.append((each,prec,rec,acc,tp,tn,fp,fn))

metric = sorted(metric,key=lambda x: x[1])
x=''
for each in metric: 
  x += 'Class %s prec %f recall %f acc %f tp %d tn %d fp %d fn %d' %each;
  x+='\n';
eval.writeintofile(x,"measurement")
