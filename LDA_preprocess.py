import sys
from gensim import corpora, models, similarities
i=0

if(len(sys.argv)!=4):
    print "USAGE python lda_preprocess.py <FILE_CONTAININTG_QUESTIONS>  <OUTPUT_FILE> <output_tags>"
    exit(1)

outfile = open(sys.argv[2],'w')
outfile_tag = open(sys.argv[3],'w')


docs = []
label_lst = []
with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        i+=1
        curr =  line[1]+' '+line[2]
        docs.append(curr.split(' '))
        label_lst.append(line[4].split(' '))

dictionary = corpora.Dictionary(docs)
print len(dictionary.token2id.items())


label_dictionary = corpora.Dictionary(label_lst)
print len(label_dictionary.token2id.items())


i=0
bow = []
for line in docs:
        curr = (dictionary.doc2bow(line))
        #print curr, line
        outfile.write( str(len(curr)) + " ")
        for a in curr:
            outfile.write(str(a[0]) + ":"+str(a[1])+" ")
        outfile.write("\n")

#print label_lst[i],label_dictionary.doc2bow (label_lst[i])
        labels  = label_dictionary.doc2bow (label_lst[i])
        for label in labels:
            outfile_tag.write(str( label[0])+ "\t")
        outfile_tag.write("\n")
        i+=1

#if(i==10):
#            break

outfile.close()
outfile_tag.close()
