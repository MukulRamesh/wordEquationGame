# from pynndescent.pynndescent_ import NNDescent
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

indexNN = NNDescent(matrix, verbose=True)
indexNN.prepare()

print("")



def wordsToVect(wordList: list[str]):
    '''Converts the string into its vectors and adds/subtracts them together'''
    operators = {'+', '-'}
    outputVector = np.zeros(vectSize, dtype=object)
    alter = '+'

    for i in range(len(wordList)):
        word = wordList[i]
        #print(word)

        if (word in operators):
            alter = word
            continue

        if (word in wordIndexDict):
            vectPart = matrix[wordIndexDict[word]]
            match alter:
                case '+':
                    outputVector += vectPart
                    #print("Added", word)

                case '-':
                    outputVector = outputVector - vectPart
                    #print("Subtracted", word)

            alter = ' '


        else:
            print("Improper String or Unknown Word")
            return -1

    return outputVector


print("Initialization Complete")

def getRandomWords(numRand: int, forbidden: list[str] = []):
    '''Takes in numRand, and an optional list of forbidden words. Returns tuple containing a numpy array that contains numRand distinct word vectors, and a list with the corresponding names'''
    outputVec = np.empty((numRand, vectSize), dtype=np.ndarray)
    outputWords = []
    for i in range(numRand):
        index = random.randint[0, numWords]
        randomWord = indexWordArray[index]

        while (randomWord in forbidden):
            index = random.randint[0, numWords]
            randomWord = indexWordArray[index]

        outputWords.append(randomWord)
        outputVec[i] = matrix[index]

        forbidden.append(randomWord)


    return outputVec, outputWords


def generateRandomAverage(numRandomWords: int, forbidden: list[str] = []):
    '''Takes in numRandomWords, and an optional list of forbidden words. Returns a list of numRandomWords+1 random words. The last word is the average of the first numRandomWords words.'''

    vectors, names = getRandomWords(numRandomWords, forbidden)

    forbidden.extend(names)
    string = ""
    for i in range(numRandomWords):
        string += names[i] + "+"

    string.strip("+")

    averageVector = wordsToVect(string) / numRandomWords

    arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
    arrayofVectors[0] = averageVector

    k = 10 + numRandomWords
    indices, distances = indexNN.query(arrayofVectors, k=k)
    outputWord = "!!None!!"

    for i in range(k):
        generatedGuess = indexWordArray[indices[0][i]][0]

        if generatedGuess in forbidden:
            continue
        else:
            outputWord = generatedGuess

    names.append(outputWord)

    return names











#"question" refers to the combo of positive and negative word vectors being added
def startCMDGame():
    '''starts a basic cmd game involving the word vecs'''
    while True:
        # for now, all generated questions will have 2 positive words and 1 negative word
        numPosWords = 2
        numNegWords = 1
        numRandWords = numPosWords + numNegWords

        print("\n\nChoosing random words...")



        ordering = [] #indicates a positive or negative word for its respective index
        for i in range(numNegWords):
            ordering.append('-')
        for i in range(numPosWords):
            ordering.append('+')
        random.shuffle(ordering)

        randWordLis = []
        indexLis = []
        inputLis = []
        for i in range(numRandWords):
            randIndex = random.randrange(0, numWords)
            indexLis.append(randIndex)
            randWordLis.append(indexWordArray[randIndex][0])

            inputLis.append(ordering[i])
            inputLis.append(randWordLis[i])
            print(i, ":", randWordLis[i])

        sumVector = wordsToVect(inputLis)

        arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
        arrayofVectors[0] = sumVector

        k = 10 + numRandWords
        indices, distances = indexNN.query(arrayofVectors, k=k)
        outputWord = "!!None!!"

        for i in range(k):
            generatedGuess = indexWordArray[indices[0][i]][0]

            if generatedGuess in randWordLis:
                continue
            else:
                outputWord = generatedGuess

        print("= :", outputWord)


        print("There are", numNegWords, "-'s and", numPosWords, "+'s.")

        while True:
            try:
                correctFlag = True
                wordList = input("Input the digits that correspond with the words, with + or - (for example: +0 +1 -2): ").split(" ")
                for word in wordList:
                    order = word[0]
                    wordNum = int(word[1])

                    if ordering[wordNum] != order:
                        print("Oh no! Looks like your answer was incorrect. Try again...")
                        correctFlag = False
                        break

                if correctFlag:
                    print("Great job! You got it correct.")
                    break

            except not KeyboardInterrupt:
                print("Incorrect formatting. Make sure the format is followed correctly.")


