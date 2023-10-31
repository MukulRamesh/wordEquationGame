import pynndescent.pynndescent_
import numpy as np
import random

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

indexNN = pynndescent.NNDescent(matrix, verbose=True)
indexNN.prepare()

print("")


#converts the string into its vectors and adds/subtracts them together
def wordsToVect(wordList: list[str]):
    operators = {'+', '-'}
    outputVector = np.zeros(vectSize, dtype=object)
    alter = '+'

    for i in range(len(wordList)):
        word = wordList[i]

        if (word in operators):
            alter = word
            continue

        if (word in wordIndexDict):
            vectPart = matrix[wordIndexDict[word]]
            match alter:
                case '+':
                    outputVector += vectPart
                    print("Added", word)

                case '-':
                    outputVector = outputVector - vectPart
                    print("Subtracted", word)

            alter = ' '


        else:
            print("Improper String or Unknown Word")
            return -1

    return outputVector

# while True:
#     wordList = input("Input space delinated string, using operators (+, -): ").split(" ")

#     arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
#     arrayofVectors[0] = wordsToVect(wordList)

#     k = 10
#     indices, distances = indexNN.query(arrayofVectors, k=k)

#     for i in range(k):
#         print(indexWordArray[indices[0][i]], distances[0][i])

#     print("\n")

print("Initialization Complete")


#"question" refers to the combo of positive and negative word vectors being added

while True:
    # for now, all generated questions will have 2 positive words and 1 negative word
    numPosWords = 2
    numNegWords = 1
    numRandWords = numPosWords + numNegWords

    print("Choosing random words...")
    randWordLis = []
    for i in range(numRandWords):
        randIndex = random.randrange(0, numWords)
        randWordLis.append(indexWords)



    wordList = input("Input the digits that correspond with the words, with + or - (for example: +1 +2 -3): ").split(" ")
