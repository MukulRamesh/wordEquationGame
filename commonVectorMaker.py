import numpy as np


nounFile = open("./parts/NOUN_POS.txt", "r")
adjFile = open("./parts/ADJ_POS.txt", "r")
verbFile = open("./parts/VERB_POS.txt", "r")

files = {nounFile, adjFile, verbFile}
dictList = list()
indexList = list()
matrixList = list()

for f in files:
    print("Loading file:", f.name, "...")
    sizeStr = f.readline().split(" ")

    numWords = int(sizeStr[0])
    vectSize = int(sizeStr[1])

    matrix = np.empty((numWords, vectSize), dtype=np.ndarray)
    wordIndexDict = dict()
    indexWordArray = np.empty((numWords, 1), dtype=np.ndarray)

    for i in range(numWords):
        strList = f.readline().split(" ")
        vector = np.empty(vectSize, dtype=object)

        wordPlain = strList[0].split("_")[0]

        wordIndexDict[wordPlain] = i
        indexWordArray[i] = wordPlain

        for j in range(vectSize):
            vector[j] = float(strList[j + 1])

        matrix[i] = vector


        if (i % 1000 == 0):
            print(i, '/', numWords)

    f.close()

    dictList.append(wordIndexDict)
    indexList.append(indexWordArray)
    matrixList.append(matrix)

def checkIfWordExists(word: str):
    for i in range(len(dictList)):
        if word in dictList[i]:
            return matrixList[i][dictList[i][word]]

    return -1

print("Creating Common Words Matrix...")

commonWordsFile = open("./commonWords100k.txt", "r", encoding='utf-8')
matrixCommon = open("./commonMatrix.txt", "w")

for line in commonWordsFile:

    # print(line.strip())


    if (line.startswith("#!comment:")):
        print(line.strip())
        continue

    word = line.strip()

    check = checkIfWordExists(word)
    if (type(check) != int):
        output = word + ' ' + ' '.join(map(str, check)) + "\n"
        matrixCommon.write(output)


commonWordsFile.close()
matrixCommon.close()

print("done.")
