import numpy as np
import sys

def closestNeighbor(vector, matrix: np.ndarray) -> int: #returns a vector within the matrix that is closest neighbor to the given vector, and the diff squared
    minIndex = -1
    minDiff = sys.maxsize
    for i in range(matrix.size):
        diff = diffSquare(vector, matrix[i])
        if (diff < minDiff):
            minIndex = i
            minDiff = diff

    return matrix[minIndex], minDiff

def diffSquare(vector1, vector2) -> int: #returns a value representing how similar 2 vectors are. 0 is the same vector, higher values indicate a larger difference
    sumval = 0
    for i in range(300):
        j = i + 1
        sumval += (vector1[j] - vector2[j]) ** 2
    return sumval

name = "ADP_POS.txt"
print("Loading file: " + name)

f = open("./parts/" + name, "r")
sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

matrix = np.empty(numWords, dtype=np.ndarray)

for i in range(numWords):
    strList = f.readline().split(" ")
    vector = np.empty(vectSize + 1, dtype=object)

    vector[0] = strList[0]

    for j in range(vectSize):
        vector[j + 1] = float(strList[j + 1])

    matrix[i] = vector

    print(i, '/', numWords, name)

f.close()

print("done loading file " + name)

print("finding combos")

#for every word, do some operator at all words. find the closest neighbor to the operator's output.

outputFile = open("./partsCombo/add/" + name, "w")

for i in range(numWords):
    for j in range(numWords):
        vector1 = matrix[i]
        vector2 = matrix[j]

        #here, TODO switch out the operator for other ones...
        newV = vector1 + vector2

        solution, sqDiff = closestNeighbor(newV, matrix)

        stringOut = vector1[0] + " + " + vector2[0] + " = " + solution[0]

        outputFile.write(stringOut + " " + str(sqDiff) + "\n")

    print(vector1[0])


