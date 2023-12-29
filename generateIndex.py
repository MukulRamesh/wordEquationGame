from pynndescent.pynndescent_ import NNDescent
import numpy as np
import pickle

print("Loading file...")

f = open("./commonMatrix.txt", "r")
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


fileName = 'CommonMatrixIndex.bin'
dbfile = open(fileName, 'ab')
pickle.dump(indexNN, dbfile)
dbfile.close()

print()
print("Index stored in", fileName)