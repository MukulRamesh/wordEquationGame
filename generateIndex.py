from pynndescent.pynndescent_ import NNDescent
import numpy as np
import pickle

print("Loading file...")

f = open("./cleanCommonMatrix.txt", "r")
sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

matrix = np.empty((numWords, vectSize), dtype=np.ndarray)
wordIndexDict = dict()
indexWordArray = np.empty((numWords, 1), dtype=np.ndarray)


for i in range(numWords):
    strList = f.readline().split(" ")
    vector = np.empty(vectSize, dtype=object)

    wordIndexDict[strList[0]] = i
    indexWordArray[i] = strList[0]

    for j in range(vectSize):
        vector[j] = float(strList[j + 1])

    matrix[i] = vector

    if (i % 1000 == 0):
        print(i, '/', numWords)

print("Matrix shape:", matrix.shape)

indexNN = NNDescent(matrix, verbose=True)
indexNN.prepare()


indexFileName = 'CommonMatrixIndex.bin'
matrixFileName = 'Matrix.bin'
wordIndexFileName = 'WordToIndex.bin'
indexWordFileName = 'IndexToWord.bin'

dbfile = open(indexFileName, 'wb')
pickle.dump(indexNN, dbfile)
dbfile.close()

dbfile = open(matrixFileName, 'wb')
pickle.dump(matrix, dbfile)
dbfile.close()

dbfile = open(wordIndexFileName, 'wb')
pickle.dump(wordIndexDict, dbfile)
dbfile.close()

dbfile = open(indexWordFileName, 'wb')
pickle.dump(indexWordArray, dbfile)
dbfile.close()

print()
print("IndexedMatrix stored in", indexFileName)
print("Matrix stored in", matrixFileName)
print("WordIndex stored in", wordIndexFileName)
print("IndexWord stored in", indexWordFileName)

