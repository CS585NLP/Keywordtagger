from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import feature
import load
import eval
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
#from sklearn.neural_network import MLPClassifier
#from random import shuffle
import numpy as np
import sys
from sklearn import cross_validation
from full_model_2 import *

import pickle
M1 = pickle.load(open("full_LR","rb"))
keywordlist = pickle.load(open("keyword_lists","rb"))
eval.evaluate([(M1,u'BOW_NN.csv')],set(list(keywordlist)[:10]));