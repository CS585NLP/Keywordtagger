#!/home/gowthamrang/anaconda/bin

#For running sample models will be soon overridden

#Split set 
import os
from random import shuffle
import csv

#from future import division

fieldnames = ['Id', 'Title', 'Body', 'Tags'];
PATH_TO_DATA = r"/home/gowthamrang/Desktop/IntrotoNLP/project/data"
TRAIN_DIR = os.path.join(PATH_TO_DATA, "train")
TEST_DIR = os.path.join(PATH_TO_DATA, "test")
DEV_DIR = os.path.join(PATH_TO_DATA, "dev")

FILE = os.path.join(PATH_TO_DATA,"small_train.csv");

def write_to_file(samples,fname):
	assert(fieldnames !=[]);
	print samples[0],'\n'+'\n'+'\n';
	#Question and paragraph 
	with open(fname, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for [i,x,y,z] in samples:
			writer.writerow({fieldnames[0]: i,fieldnames[1]: x, fieldnames[2]: y, fieldnames[3]:z})
    




examples =[];
s=set();
with open(FILE) as csvfile:
	KeywordTagger = csv.DictReader(csvfile);
	
	for row in KeywordTagger:
		if row[fieldnames[0]] == None:
			row[fieldnames[0]] = '';
		if row[fieldnames[1]] == None:
			row[fieldnames[1]] = '';
		if row[fieldnames[2]] == None:
			row[fieldnames[2]] = '';
		if row[fieldnames[3]] == None:
			row[fieldnames[3]] = '';
		examples.append([row[fieldnames[0]],row[fieldnames[1]],row[fieldnames[2]],row[fieldnames[3]]]);
		s.update(set(row[fieldnames[3]]));

shuffle(examples);

x=6*len(examples)/10
y=x/3;

train= examples[:x];
dev = examples[x:x+y];
test = examples[x+y:];

write_to_file(train,os.path.join(TRAIN_DIR,'train_reduced.csv'));
write_to_file(examples[x:x+y],os.path.join(DEV_DIR,'dev_reduced.csv'));
write_to_file(test,os.path.join(TEST_DIR,'test_reduced.csv'));

print len(s)