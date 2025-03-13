import enchant
from nltk.stem import WordNetLemmatizer as wnl
d = enchant.Dict("en_US")


print("Loading bad words...")

bads = set(line.strip() for line in open('./badWords.txt'))

print("Loading/Filtering commonMatrix...")

f = open("./commonMatrix.txt", "r")
outFile = open("./cleanCommonMatrix.txt", "w")

sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

seenLemmas = set()

for i in range(numWords):
    strList = f.readline().split(" ")
    wordText = strList[0]

    if ((len(wordText) > 2) and (wordText not in bads) and (d.check(wordText)) and (wnl().lemmatize(wordText) not in seenLemmas)):
        lemma = wnl().lemmatize(wordText)
        seenLemmas.add(lemma)
        strList[0] = lemma
        outFile.write(" ".join(strList))

    if (i % 1000 == 0):
        print(i, '/', numWords)



# Currently this generates a file that is slightly too large: the current solution is to truncate the file so that the last 100 or so entries are removed.

