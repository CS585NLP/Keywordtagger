import scipy.sparse as sps
from collections  import defaultdict



#Simple feature
def BOW_features(title,description,code):
	sentence = title+description;
	s = sentence.split(' ');
	d= defaultdict(float);
	for each in s:d[each.lower()]+=1
	return d;

def BOW_TRIM_features(title,description,code):
	d= defaultdict(float);
	for each in title.split(' '):d[each.lower()]=1
	return d;

def BOW_features_title_body(title,description,code):
    d= defaultdict(float);
    for each in title.split(' '):d[each.lower()+"title"]+=1
    for each in description.split(' '):d[each.lower()+"body"]+=1
    return d;

def BOW_features_title_body_bigram(title,description,code):
    d= defaultdict(float);
    for each in title.split(' '):d[each.lower()+"title"]+=1
    desc = description.split(' ')
    for each in desc:d[each.lower()+"body"]+=1
    for i in range(len(desc)-1):
        d[desc[i]+"_"+desc[i+1]]+=1
    return d;

def BOW_features_bigram_rules(title,description,code):
    d= defaultdict(float);
    for each in title.split(' '):d[each.lower()+"title"]+=1
    desc = description.split(' ')
    for each in desc:d[each.lower()+"body"]+=1
    for i in range(len(desc)-1):
        d[desc[i]+"_"+desc[i+1]]+=1
    if("#include" in code):
        d["c"]=1
    if("def" in code):
        d["python"]=1


    return d;


class feature:
    def BOW_keyword_only(self,title,description,code):
        
        d= defaultdict(float);
        for each in description.split(' '):
            if each.lower() in self.keywords :
                d[each.lower()]+=1;
        for each in title.split(' '):
            if each.lower() in self.keywords:
                d[each.lower()]+=1;
        return d;
	
    def __init__(self, featurename,Train,keywords=None):
        self.supportedfeatures = ['bow','bow_trimmed','bow_separate','bow_bigram','bow_keyword_only','bow_rules'];
        assert(featurename in self.supportedfeatures)
        self.featurename = featurename.lower(); # ALL IN Lowercase
        self.Train = Train;
        self.keywords = keywords;
        print keywords
        #self.test = test;
        self.feature_list = {};
        self.FEATURE_MODEL = None;
    
        if self.featurename == 'bow':
            print 'BOW representation is being used'
            self.FEATURE_MODEL = BOW_features;
        elif self.featurename == 'bow_trimmed':
            print 'BOW_trimmed representation is being used'
            self.FEATURE_MODEL = BOW_TRIM_features;
        elif self.featurename == 'bow_separate':
            print 'BOW_separate representation is being used'
            self.FEATURE_MODEL = BOW_features_title_body;
        elif self.featurename == 'bow_bigram':
            print 'BOW_bigram representation is being used'
            self.FEATURE_MODEL = BOW_features_title_body_bigram;
        elif self.featurename == 'bow_rules':
            print 'BOW_bigram representation is being used'
            self.FEATURE_MODEL = BOW_features_bigram_rules;
        elif self.featurename == 'bow_keyword_only':
            self.FEATURE_MODEL = self.BOW_keyword_only;
        else:
			assert(False);
        self.init_feature_set();


    def init_feature_set(self):
		print self.Train[0]       
		
		for each in self.Train:
			for each_activation in self.FEATURE_MODEL(each[1],each[2],each[3]): self.feature_list[each_activation] = 0;
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
        
            featactivation = self.FEATURE_MODEL(each[1],each[2],each[3]);
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

					
