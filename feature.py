import scipy.sparse as sps
from collections  import defautldict



#Simple feature
def BOW_features(title,description):
	sentence = title+description;
	s = sentence.split(' ');
	d= defaultdict(float);
	for each in s:d[lower(each)]+=1
	return d;

class feature:
	supportedfeatures = ['BOW_lcasespacesep'];
	def __init__(self, featurename,Train,Test):
		assert(featurename in self.supportedfeatures)
		self.featurename = lower(featurename); # ALL IN Lowercase
		self.train = train;
		self.test = test;
		self.feature_list = {};
		self.FEATURE_MODEL = None;
		
		if self.featurename == 'bow':				
			self.FEATURE_MODEL = BOW_features;
		else:
			assert(False);
		self.init_feature_set();


	def init_feature_set(self):
		
		for each in self.train:
			for each_activation in self.FEATURE_MODEL(each[1],each[2]): feature_list[each_activation] = 0;
		for pos,each_activation in enumerate(feature_list): feature_list[each_activation] = pos;

		print "The number of features according to %s feature Model is %d", (self.feature_name,len(self.feature_list));
		return;


	#for mini batch
	def get_incremental_features(self,examples,type='For caching this batch'):
		#do caching if you wish
		#needs to be changed if we want to run on large dataset .... something like build feature_list on thefly, then we need to distinguish test and train features()
		assert(type(type)==str);
		assert(self.feature_list !={});
		assert(self.FEATURE_MODEL !=None);

		X = sps.coo_matrix((len(self.examples), cols))		

		for each in examples:
			type(each[1]==str and type(each[2])== str);
			feature_data=[]
			feature_data_location=[];
			
			featactivation = self.FEATURE_MODEL(each[1]+each[2]);					
			for each_activation in featactivation:
				assert(featactivation[each_activation] != 0);
				feature_data.append(featactivation[each_activation])
			
			X =  X + sps.coo_matrix((feature_data, ([exampleno]*len(self.feature_list),
					 feature_list[each_activation])), shape=(len(self.exampleno), len(self.feature_list)))
		return X;




if __name__ == '__main__':
	#test();

					