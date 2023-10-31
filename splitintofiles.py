import numpy as np

print("Loading file...")

#maybe seperate model into categories, each with its own text file.
f = open("model.txt", "r")
sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

partToFile = dict()

for i in range(numWords):
    strList = f.readline().split(" ")
    word, participle = strList[0].split("_")

    if (participle not in partToFile):
        file = open("./parts/" + participle + "_POS.txt", "w")
        partToFile[participle] = file


    partToFile[participle].write(' '.join(strList))
    print(word, participle, i, "/", numWords)



print("done.")