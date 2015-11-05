from SplitTest import fieldnames

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
z = open(DEV_FILE)
x.close();
y.close();
z.close();

import csv


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
		for no,row in enumerate(KeywordTagger):		
			if (numdocs !=None):
				if(no>=numdocs): 
					break;
			examples.append([row[fieldnames[0]],row[fieldnames[1]],row[fieldnames[2]]]);
			tags.append(row[fieldnames[3]].split(' ')); #tags are space seperated	
			
	return examples,tags
		
import numpy as np
#Binary classifier
def split_equally(classname,X,train_target):

	target_y = [1 if classname in x  else 0 for x in train_target ];
	target_y_positive = filter(lambda (x): x[1]==1, enumerate(target_y))
	target_y_negative = filter(lambda (x): x[1]==0, enumerate(target_y))
	target_y_negative = target_y_negative[:len(target_y_positive)]
	sampleno = [];
	for ex,each in target_y_positive: sampleno.append(ex);
	for ex,each in target_y_negative: sampleno.append(ex);

	target_y = [1]*len(target_y_positive)
	target_y.extend([0]*len(target_y_negative))
	print X.toarray()[sampleno,:]
	return [np.array(target_y), X.toarray()[sampleno,:]]