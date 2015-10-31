#!/home/gowthamrang/anaconda/bin

#NBClassifier with BOW model max likelhood training

from __future__ import division

import math
import os

from collections import defaultdict
from math import *
from random import shuffle

from sklearn.naive_bayes import MultinomialNB

import Feature


# Global class labels.
POS_LABEL = 'pos'
NEG_LABEL = 'neg'

# Path to dataset
PATH_TO_DATA = r"/home/gowthamrang/Desktop/IntrotoNLP/project/data"

TRAIN_DATA = os.path.join(PATH_TO_DATA, "train")
TEST_DATA = os.path.join(PATH_TO_DATA, "test")

#Modify this to include entire dataset
TRAIN_FILE_NAME = "train_reduced.csv";
DEV_FILE_NAME = "dev_reduced.csv";

#'duck testing'
assert(TRAIN_FILE_NAME[-4:].lower() == '.csv' and DEV_FILE_NAME[-4:].lower()=='.csv')

#data can be weights or features but they are a list
def load(data,fname='BOWmodel_train'):
	assert(type(data) == list and type(fname) == str);



_examples = load(Train=True,num_docs = 2000);
dev_set = load(num_docs=500);

#last is tags in examples
permute(_examples);

for each in _examples:
  examples.append(each[:-1])
  target.append(each[-1]);

bow = Feature.feature("bow",examples,dev_set);

example_features = bow.get_incremental_features(examples);

classes = set(target);
classifyers =[];

for each in classes:
  Y = np.array([1 if x == each else 0 for x in target ]);
  clf = GaussianNB();
  clf.fit(X,Y);
  classifyers.append(clf);

pred = [];
for i,keyword in enumerate(classes):
  pred = classifyers[i].predict(Dev);
  pred.append([]);
  for exampleno,each in enumerate(pred):
    if each == 1:
      pred[exampleno].append(keyword);


import eval
print eval.fscore(gold,pred);


#batch-learning
#from sklearn.naive_bayes import GaussianNB

