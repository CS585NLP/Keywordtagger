# Keywordtagger
dependencies scikitlearn

The pipeline is expected to work as follows<br>
1.unclean data ---->[text_cleaner.py]---->cleandata <br>
2.cleandata ------->[SplitTest.py]-----> [test,dev,train] datasets<br>
3.Model:- bayes_unigram.py<br>
  3.1 [traindataset]--------->feature.py-------->[features for trainset]<br>
  3.2 [features for trainset]------->[trained model]<br>
  3.3 [testdataset]---------->feature.py-------->[test features]<br>
  3.4 [features for testset]------->classify [predicted result]<br>


## observations:
Tags are sparse.[1000 tags]. so model finds it hard to predict 

##How to run.
if necessary change the input dataset in Splittest.py , run it 
then run bayes_unigram.py
