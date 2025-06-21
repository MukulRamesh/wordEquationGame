from nltk.stem import WordNetLemmatizer as wnl
from nltk.stem import PorterStemmer as ps
import enchant
d = enchant.Dict("en_US")


print("Loading bad words...")

bads = set(line.strip() for line in open('./badWords.txt'))

print("Loading/Filtering commonMatrix...")

f = open("./commonMatrix.txt", "r")
outFile = open("./cleanCommonMatrix.txt", "w")

sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

seenWords = set()

for i in range(numWords):
    strList = f.readline().split(" ")
    wordText = strList[0]

    lemma = wnl().lemmatize(wordText)
    stem = ps().stem(lemma)

    if ((len(stem) > 2) and (stem not in bads) and (d.check(stem)) and (stem not in seenWords)):
        seenWords.add(stem)
        strList[0] = stem
        outFile.write(" ".join(strList))

    if (i % 1000 == 0):
        print(i, '/', numWords)
