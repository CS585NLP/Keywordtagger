#!/home/gowthamrang/anaconda/bin

#NBClassifier with BOW model max likelhood training

from __future__ import division

import feature
import load
import eval
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import numpy as np

LOGISTIC_REGRESSION = True;

if LOGISTIC_REGRESSION:
  print 'LogisticRegression is Active';
else:
  print 'NB is Active';

print 'Begin Loading samples...'
#load samples
train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=None);
dev_samples,dev_target = load.load_dataset(fname=load.filename['DEV'],numdocs=None);
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

#Feature Model
if not LOGISTIC_REGRESSION:
  bow = feature.feature("bow",train_samples);
  X = bow.get_incremental_features(train_samples);
else:
  bow_trimmed = feature.feature("bow_trimmed",train_samples);
  X = bow_trimmed.get_incremental_features(train_samples);


#for each in classes:
 #returns a copy
# Ynew,Xnew = load.split_equally(each,X,train_target);
# assert(Xnew.shape[0] ==  Ynew.shape[0])
# assert(X.shape[0] == len(train_target))
  #shuffle if necessary  
# clf = MultinomialNB(fit_prior=False);# onlu MultinomialNB takes sparse matrix , to offset hughe neg samples
# clf.fit(Xnew,Ynew);
# classifyers.append(clf);

#Classifier Model : Train
for each in classes:
  Y = np.array([1 if each in x  else 0 for x in train_target ]);  
  assert(X.shape[0] ==  len(train_samples))
  assert(Y.shape[0] == len(train_samples))
  if not LOGISTIC_REGRESSION:
    clf = MultinomialNB(fit_prior=False);# onlu MultinomialNB takes sparse matrix , to offset hughe neg samples
  else:
    clf = LogisticRegression();
  clf.fit(X,Y);
  classifyers.append(clf);

#Classifier Model: Test
metric = [];
if not LOGISTIC_REGRESSION:
  X_dev = bow.get_incremental_features(dev_samples,Train=False);
else:
  X_dev = bow_trimmed.get_incremental_features(dev_samples,Train=False);

print 'Testing for %d dev samples',len(dev_samples)
for classifyerno,eachclassifier in enumerate(classes):
  print 'Classifying %s',eachclassifier
  Y_dev = classifyers[classifyerno].predict(X_dev);
  gold = [ 1 if eachclassifier in x else 0 for x in dev_target]
  pred = Y_dev.tolist()
  [prec,rec,acc,tp,tn,fp,fn] = eval.precision_recall_per_class(gold,pred)
  eval.confused_examples(dev_target,dev_samples,gold,pred,3)
  metric.append((eachclassifier,prec,rec,acc,tp,tn,fp,fn))

metric = sorted(metric,key=lambda x: x[1])
for each in metric: 
  print 'Class %s prec %f recall %f acc %f tp %d tn %d fp %d fn %d' %each;

#print zip(dev_target,pred)
#pred_tags = ['']*len(dev_samples)

#for i,keyword in enumerate(classes):
#  Y_dev = classifyers[i].predict(X_dev);
#  for exampleno,each in enumerate(Y_dev.tolist()): 
#  	if each>0 :
#  		pred_tags[exampleno]+=' '+keyword; #space seperated tags
  
#pred_tags = [each.split(' ')for each in pred_tags]
#print 'predicting precision recall for %d examples each class' %len(dev_target)
#gold = [0]*len(dev_target);
#pred = [0]*len(pred_tags);

#for eachclass in classes:
#  for sampleno,sample_tags in enumerate(dev_target): gold[sampleno] = 1 if eachclass in sample_tags else 0;
#  for sampleno,eachpred_tags in enumerate(pred_tags): pred[sampleno] = 1 if eachclass in eachpred_tags else 0;  
#  print zip(gold,pred)
#  print 'Results for tag %s' %eachclass
#  eval.precision_recall_per_class(gold,pred);
