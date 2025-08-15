import math
import re
import csv
from collections import defaultdict
from collections import Counter

def preproc(f):
    with open(f) as file:
        updates = []
        lines = file.readlines()
    for line in lines:
        line = re.sub(r"[^\w\s]", '', line)
        line = re.sub('\s+', ' ', line).strip()
        line = re.sub(r"https?://\S+", '', line)
        line = line.lower()
        updates.append(line)
    stopwords = []
    with open('stopwords.txt') as stopwordsfile:
        words = stopwordsfile.read()
        stopwords = words.split()
    cleaned = []
    for line in updates:
        words = line.split()
        words = [word for word in words if word not in stopwords]
        cleaned.append(" ".join(words))
    stemmed = []
    for line in cleaned:
        words = [re.sub(r"(ing|ly|ment)\b", '', word) for word in line.split()]
        stemmed.append(" ".join(words))
    outputname = 'preproc_' + f
    with open(outputname, 'w') as outputfile:
        for line in stemmed:
            outputfile.write(line + '\n')
    
    return outputname


def tf(f):
    with open(f) as file:
        wordbank = []
        lines = file.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            wordbank.append(word)
    tf = {}
    counter = Counter(wordbank)
    for word, count in counter.items():
        tf[word] = count/len(wordbank)
    return tf


def main():
    idf = {}
    count = defaultdict(int)
    source = defaultdict(list)
    outputs = []
    with open('tfidf_docs.txt') as docs:
        docnames = [line.strip() for line in docs.readlines()]
    for docname in docnames:
        output = preproc(docname)
        outputs.append(output)
    for output in outputs:
        sample = tf(output)
        for key in sample:
            source[output].append(key)
    for file in source:
        for word in source[file]:
            count[word] += 1
    for word in count:
        idf[word] = math.log(len(outputs)/count[word]) + 1
    
    for output in outputs:
        sample = tf(output)
        tfidf = {}
        for word in sample:
            tfidf[word] = round((sample[word] * idf[word]), 2)
        tfidf = dict(sorted(tfidf.items(), key=lambda x: (-x[1], x[0])))
        outputname = 'tfidf_' + output.split("_", 1)[-1]
        with open(outputname, 'w') as outputfile:
            outputfile.write(str(list(tfidf.items())[:5]) + '\n')
    




    pass
    
main()