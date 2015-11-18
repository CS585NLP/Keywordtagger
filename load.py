from SplitTest import fieldnames
from random import shuffle
#cleaned and well shuffled dataset
#TRAIN_FILE = r'data/train/train_reduced_cleaned.csv'
#DEV_FILE = r'data/dev/dev_reduced_cleaned.csv'
#TEST_FILE = r'data/test/test_reduced_cleaned.csv'

#for now
TRAIN_FILE = r'data/train/train_reduced.csv'
DEV_FILE = r'data/dev/dev_reduced.csv'
TEST_FILE = r'data/test/test_reduced.csv'


filename = {'TRAIN':TRAIN_FILE,'DEV':DEV_FILE,'TEST':TEST_FILE}

x =open(TRAIN_FILE)
y = open(TEST_FILE)
#z = open(DEV_FILE)
x.close();
y.close();
#z.close();

import csv
from collections import defaultdict


def load_dataset(fname=filename['TRAIN'],numdocs=None):
	"""
	Loads a cleaned dataset and gives out examples and tags"""

	if numdocs != None:
		print "Loading %d docs from File %s " %(numdocs,fname)
	else:
		print "Loading all docs from File %s " %(fname)
	examples =[];
	tags=[]

	with open(fname) as csvfile:
		KeywordTagger = csv.DictReader(csvfile);
		for no,row1 in enumerate(KeywordTagger):		
			if (numdocs !=None):
				if(no>=numdocs): 
					break;
			row = defaultdict(lambda : '', row1);
			examples.append([row[fieldnames[0]],row[fieldnames[1]],row[fieldnames[2]],row[fieldnames[3]]]);
			tags.append(row[fieldnames[4]].split(' ')); #tags are space seperated	
			
	return examples,tags
		
import numpy as np
#Binary classifier
def split_equally(target_label, samples):	
	target_label_positive = filter(lambda (x): x[0]==1, zip(target_label,samples))
	target_label_negative = filter(lambda (x): x[0]==0, zip(target_label,samples))
  	

	target_label_negative = target_label_negative[:len(target_label_positive)];
	#shuffle(target_label_negative)
	#shuffle(target_label_positive)

	target_label_positive,train_positive =zip(*target_label_positive);
	target_label_positive,train_positive  = list(target_label_positive), list(train_positive)
	target_label_negative,train_negative =zip(*target_label_negative);
	target_label_negative,train_negative = list(target_label_negative), list(train_negative)

	train_positive.extend(train_negative); 
	target_label_positive.extend(target_label_negative);
	d = zip(target_label_positive,train_positive);
	shuffle(d)
	[target_label_positive, train_positive] = zip(*d);
	target_label_positive = list(target_label_positive)
	train_positive = list(train_positive)
	del d;

	return target_label_positive,train_positive
	  
