#!/home/gowthamrang/anaconda/bin

#NBClassifier with BOW model max likelhood training

from __future__ import division

import feature
import load
import eval
from sklearn.naive_bayes import MultinomialNB
import numpy as np

print 'Begin Loading samples...'
#load samples
train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=10000);
dev_samples,dev_target = load.load_dataset(fname=load.filename['DEV'],numdocs=10);

print 'Tags for the last train example',train_target[-1]
#print train_target
#print train_samples[0]
#Classifier Model
classes=[];
for each in train_target: classes.extend(x for x in each);
classes = set(classes);
classifyers =[];
print 'Total number of classes for this model ', len(classes)

class_example_count = [];
for each in classes:
  Y = np.array([1 if each in x  else 0 for x in train_target ]); 
  class_example_count.append(sum(Y));
print 'examples seen for each class during training ' ,class_example_count
#assert(False)

#Feature Model
bow = feature.feature("bow",train_samples);
X = bow.get_incremental_features(train_samples);



#Classifier Model : Train
for each in classes:
  Y = np.array([1 if each in x  else 0 for x in train_target ]); 
  assert(X.shape[0] ==  len(train_samples))
  assert(Y.shape[0] == len(train_samples))
  clf = MultinomialNB();# onlu MultinomialNB takes sparse matrix 
  clf.fit(X,Y);
  classifyers.append(clf);

#Classifier Model: Test
X_dev = bow.get_incremental_features(dev_samples,Train=False);
pred = ['']*len(dev_samples)

for i,keyword in enumerate(classes):
  Y_dev = classifyers[i].predict(X_dev);
  for exampleno,each in enumerate(Y_dev.tolist()): 
  	if each>0 :
  		pred[exampleno]+=' '+keyword; #space seperated tags
  

print zip(dev_target,pred)
#print eval.fscore(dev_target,pred);


