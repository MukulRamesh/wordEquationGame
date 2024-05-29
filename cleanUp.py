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

for i in range(numWords):
    strList = f.readline().split(" ")

    if ((len(strList[0]) > 2) and (strList[0] not in bads) and (d.check(strList[0]))):
        outFile.write(" ".join(strList))

    if (i % 1000 == 0):
        print(i, '/', numWords)


