from HTMLParser import HTMLParser
from nltk.corpus import stopwords
import string
import itertools,re

class Cleaner:
    def __init__(self):
        self.html_parser = HTMLParser()
        self.APPOSTOPHES = {"'s" : " is", "'re" : " are","'ll":" will","'d":" would", "'m":" am"}
        self.slangs={}
        for line in open('slangs.txt'):
            sp=line.strip().split("-")
            self.slangs[sp[0]]=sp[1]
        self.stopwords = set(stopwords.words('english'))
        self.punc = set(string.punctuation)
    
    def clean(self,text):
        return ((self.removeUrl(self.standardize(self.splitAttachedWords(self.removePunc((self.correctAppostophe(self.decode(self.unescape(self.replaceSlangs(text)))))))))).lower())
    
    #return self.removeShortWords(self.removeStopWords((self.removeUrl(self.standardize(self.splitAttachedWords(self.removePunc((self.correctAppostophe(self.decode(self.unescape(self.replaceSlangs(text)))))))))).lower()))
        
    def removeShortWords(self,text):
        return ' '.join(word for word in text.split() if len(word)>=3)
        
    def unescape(self,text):
        return self.html_parser.unescape(text)
        
    def decode(self,text):
        return text.decode('utf8').encode('ascii','ignore')
        
    def correctAppostophe(self,text):
        t=text
        for appostophe in self.APPOSTOPHES:
            if appostophe in t:
                t=t.replace(appostophe,self.APPOSTOPHES[appostophe])
        return t
    
    def removeStopWords(self,text):

        words=text.split()
        return ' '.join(word for word in words if word not in self.stopwords)
    
    def removePunc(self,text):
		textnew=''
		for ch in text:
				if ch not in self.punc:
					textnew=textnew+ch
				else:
					textnew=textnew+' '
		words=textnew.split()
		return ' '.join(word for word in words)
    
    def splitAttachedWords(self,text):
        return " ".join(re.findall('[A-Za-z][^A-Z]*', text))
    
    def replaceSlangs(self,text):
        words=text.split()
        l=[]
        for word in words:
            if word not in self.slangs:
                l.append(word)
            else:
                l.append(self.slangs[word])
        return ' '.join(l)
    
    def standardize(self,text):
        return ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))   
    
    def removeUrl(self,text):
        return ' '.join(word for word in text.split() if not word.startswith("http"))


def clean_question(title,answer):
    c=Cleaner()
    clean_title = c.clean(title)
    clean_ans = c.clean(answer)
    return [clean_title.split(), clean_ans.split()]


print clean_question("how are u doing ? ??","I'm a nice guy</br>")
