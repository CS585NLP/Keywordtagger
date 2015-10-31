import scipy.sparse as sps
from collections  import defaultdict



#Simple feature
def BOW_features(title,description):
	sentence = title+description;
	s = sentence.split(' ');
	d= defaultdict(float);
	for each in s:d[each.lower()]+=1
	return d;

class feature:
	
	def __init__(self, featurename,Train):
		self.supportedfeatures = ['bow'];
		assert(featurename in self.supportedfeatures)
		self.featurename = featurename.lower(); # ALL IN Lowercase
		self.Train = Train;
		#self.test = test;
		self.feature_list = {};
		self.FEATURE_MODEL = None;
		
		if self.featurename == 'bow':				
			self.FEATURE_MODEL = BOW_features;
		else:
			assert(False);
		self.init_feature_set();


	def init_feature_set(self):
		
		for each in self.Train:
			for each_activation in self.FEATURE_MODEL(each[1],each[2]): self.feature_list[each_activation] = 0;
		for pos,each_activation in enumerate(self.feature_list): self.feature_list[each_activation] = pos;


		print "The number of features according to %s feature Model is %d" %(self.featurename,len(self.feature_list));
		return;


	#for mini batch
	def get_incremental_features(self,examples,Type='For caching this batch',Train=True):
		#do caching if you wish
		#needs to be changed if we want to run on large dataset .... something like build feature_list on thefly, then we need to distinguish test and Train features()
		assert(type(Type)==str);
		assert(self.feature_list !={});
		assert(self.FEATURE_MODEL !=None);

		X = sps.coo_matrix((len(examples), len(self.feature_list)))		

		for exampleno,each in enumerate(examples):
			type(each[1]==str and type(each[2])== str);
			feature_data=[]
			feature_data_location=[];
			
			featactivation = self.FEATURE_MODEL(each[1],each[2]);					
			for each_activation in featactivation:
				assert(featactivation[each_activation] != 0);
				try:
					self.feature_list[each_activation]					
				except KeyError:					
					if (Train): print 'WTF! should not come here ., you are using dataset different from Train!...silently dropping...'
					continue;

				feature_data.append(featactivation[each_activation])
				feature_data_location.append(self.feature_list[each_activation]);
			assert(len(feature_data_location) == len(feature_data))
			
			print '\rFinding features for example %d' %exampleno,

			X =  X + sps.coo_matrix((feature_data, ([exampleno]*len(feature_data),
					 feature_data_location)), shape=X.shape)
		print ''
		return X;




if __name__ == '__main__':
	print 'Test to be written';

					