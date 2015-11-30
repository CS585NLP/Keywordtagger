import sys
from gensim import corpora, models, similarities
corpus = []
with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.split()
        num = int(line[0])
        #       print line,num
        lst = []
        for i in range(1,num+1):
            temp = line[i].split(":")
            lst.append((int(temp[0]),int(temp[1])))
        corpus.append( lst)
#print corpus[0]

lda = LdaModel(corpus, num_topics=100)
print lda