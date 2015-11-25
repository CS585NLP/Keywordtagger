from HTMLParser import HTMLParser
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

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
        self.punc = set(string.punctuation).difference(set(['+']))
    
    def clean(self,text):
        list = self.removeStopWords(self.removeUrl(self.removePunc(self.remove_code(self.detachPunc(self.standardize(((self.correctAppostophe(((self.replaceSlangs(text))))))))))))
        text = list[0]
        code = list[1]
        return [text, code]
    
    #return self.removeShortWords(self.removeStopWords((self.removeUrl(self.standardize(self.splitAttachedWords(self.removePunc((self.correctAppostophe(self.decode(self.unescape(self.replaceSlangs(text)))))))))).lower()))
    
    def removeShortWords(self,text):
        return ' '.join(word for word in text.split() if len(word)>=3)
    
    def unescape(self,text):
        return self.html_parser.unescape(text)
    
    def decode(self,text):
        return text.decode('utf8').encode('ascii','ignore')
    def remove_code(self,text):
        
        soup = BeautifulSoup(text, 'html.parser')
        code_instances =  soup.find_all('code')
        code = ""
        for i in code_instances:
            text = text.replace(str(i),' ')
            code+=" " + str(i)
        text = soup.get_text()
        code = code.replace('<code>' , ' ')
        code = code.replace('</code>',' ')
        code = code.replace(',',' ')
        return [text, code]
    
    def correctAppostophe(self,text):
        t=text
        for appostophe in self.APPOSTOPHES:
            if appostophe in t:
                t=t.replace(appostophe,self.APPOSTOPHES[appostophe])
        return t
    
    def removeStopWords(self,text_list):
        text = text_list[0]
        code = text_list[1]
        
        words=text.split()
        return [' '.join(word for word in words if word.lower() not in self.stopwords), code]
    
    def detachPunc(self,text):
        ch='<'
        if ch in text:
            text = text.replace(ch,' '+ch)
        ch='>'
        if ch in text:
            text = text.replace(ch,ch+' ')
        return text
    
    def removePunc(self,text_list):
        text = text_list[0]
        code = text_list[1]
        textnew=''
        for ch in text:
            if ch not in self.punc:
                textnew=textnew+ch
            else:
                textnew=textnew+' '
        words=textnew.split()
        return [' '.join(word for word in words) , code]
    
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
    
    def removeUrl(self,text_list):
        text = text_list[0]
        code = text_list[1]
        return [' '.join(word for word in text.split() if not word.startswith("http")) , code]


def clean_question(title,answer):
    c=Cleaner()
    [clean_title, code_false] = c.clean(title)
    [clean_ans, code] = c.clean(answer)
    return [clean_title, clean_ans, code]

print clean_question("how are u doing ? ??","""Regex for converting file path to package/namespace","<p>Given the following file path:</p>
    
    <pre><code>/Users/Lawrence/MyProject/some/very/interesting/Code.scala
    </code></pre>
    
    <p>I would like to generate the following using a <em>single</em> regex replace (the root can be a constant):</p>
    
    <pre><code>some.very.interesting
    </code></pre>
    
    <p>This is for the purpose of generating a snippet for Sublime Text which can automatically insert the correct package/namespace header for my scala/java classes :)</p>
    
    <p>Sublime Text uses the following syntax for their regex replace patterns (aka 'substitutions'):</p>
    
    <pre><code>{input/regex/replace/flags}
    </code></pre>
    
    <p>Hence why an iterative approach cannot be taken - it has to be done in one pass! Also, substitutions <em>cannot</em> be nested :(</p>
    """)


import csv
i=0
with open('Train.csv', 'rb') as csvfile:
    file = csv.reader(csvfile, delimiter=',', quotechar='"')
    arow=["","","","",""]
    for row in file:
        arow[0]=row[0]
        [arow[1],arow[2],arow[3]] = clean_question(row[1],row[2])
        arow[4] = row[3]
        try:
            print ','.join(arow)
        except:
            i-=1
        #print ','.join(row)
        i+=1

print i