
from __future__ import division

import load
import numpy as np
import matplotlib.pyplot as plt    
from collections import defaultdict
#from pylab import pcolor, show, colorbar, xticks, yticks,xticklabels,yticklabels

from pylab import colorbar
#exploratory data analysis or data viz on train set only.

def tags_count(train_target):
	print 'tags vs number of times tag appears in %'
	classes = defaultdict(float);
	for each in train_target:
		for everytag in each:
			classes[everytag]+=1;
	s=0.0
	for each in classes: s+=classes[each];
	for each in classes: classes[each]=classes[each]/s * 100;
	q = 100.0
	y = filter(lambda x: x[1]>=q*100.0/len(train_target) ,classes.items());
	print 'plotting the %d tags that occur more than in %d questions' %(len(y), q)
	y = sorted(y, key=lambda t: -t[1]);
	x_tick,y = zip(*y)
	x = range(len(x_tick));	
	
	#print zip(x_tick,y)
	#plt.xticks(x, x_tick )
	fig, ax = plt.subplots()

	ax.set_xticks(x)
	ax.set_xticklabels(x_tick,rotation=90)
	plt.bar(x,y)	
	
	plt.xlabel('Tags')
	plt.ylabel('Occurance rate (%)')
	plt.title('Likelhood of Tags in the dataset')
	plt.show()
	return x_tick


def tags_correlation(train_target,classes):
	print 'tags correlation viz'
	correlation = defaultdict(lambda : defaultdict(float));
	for x in classes: 
		for y in classes:
			correlation[x][y] = 0.0

	for each in train_target:
		for x in each:
			if( x not in classes):
				continue;

			for y in each:
				if y not in classes:
					continue;
				correlation[x][y]+=1; #xand y occur togther


	for x in classes: 
		s=correlation[x][x];
		for y in classes:			
			correlation[x][y]/=s; 

	r=[];
	for x in correlation:
		r.append([ correlation[x][y] for y in correlation[x]])
	print len(r) == len(r[0]), r[1]
	data = np.array(r, np.float32)
	#pcolor(x)
	#xticklabels(classes);
	#yticklabels(classes)
	#colorbar();
	#show();
	fig, ax = plt.subplots()
	fig.set_size_inches(11, 11)
	heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
	cbar = plt.colorbar(heatmap)
	# put the major ticks at the middle of each cell
	ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

	# want a more natural, table-like display
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	ax.set_xticklabels(classes, minor=False,rotation=90)
	ax.set_yticklabels(classes, minor=False)
	
	plt.show()
	







def keyword_presence():
	return;



if __name__ == '__main__':
	print 'Exploratory data analysis'
	print 'Begin Loading samples...'
	train_samples,train_target = load.load_dataset(fname=load.filename['TRAIN'],numdocs=None);
	classes = tags_count(train_target);
	tags_correlation(train_target,classes)
