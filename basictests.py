import pickle
import numpy as np
import random
from scipy.spatial.distance import pdist, squareform

print("Loading file...")

f = open("./cleanCommonMatrix.txt", "r")
sizeStr = f.readline().split(" ")

numWords = int(sizeStr[0])
vectSize = int(sizeStr[1])

f.close()

matrixFileName = 'Matrix.bin'
wordIndexFileName = 'WordToIndex.bin'
indexWordFileName = 'IndexToWord.bin'

indexFileName = 'CommonMatrixIndex.bin'

print("Loading saved matrix file...")
matrix = pickle.load(open(matrixFileName, 'rb'))
print("Loading saved wordIndex file...")
wordIndexDict = pickle.load(open(wordIndexFileName, 'rb'))
print("Loading saved indexWord file...")
indexWordArray = pickle.load(open(indexWordFileName, 'rb'))
print("Loading saved index file...")
indexNN = pickle.load(open(indexFileName, 'rb'))

print("Matrix shape:", matrix.shape)
print("Done.")

print("-- Initialization Complete --")


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
            print("Improper String or Unknown Word:", word)
            raise TypeError

    return outputVector


def wiggleVector(vector: np.ndarray, forbidden, wiggleValue: int = 10, wiggleMaxMag: float = 0.3, wiggleMinMag: float = 0.2, kAppend: int = 10):
    rawWiggledVector = vector

    flag = True
    while flag == True:
        randomEntries = random.sample(range(len(vector)), wiggleValue)
        for entry in randomEntries:
            magnitudeOfWiggle = random.uniform(wiggleMinMag, wiggleMaxMag)
            rawWiggledVector[entry] += magnitudeOfWiggle * random.choice([-1, 1])


        arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
        arrayofVectors[0] = rawWiggledVector

        k = kAppend
        indices, distances = indexNN.query(arrayofVectors, k=k)
        outputWord = "!!None!!"

        for i in range(k):
            generatedGuess = indexWordArray[indices[0][i]][0]

            if (generatedGuess in forbidden):
                continue
            else:
                outputWord = generatedGuess
                flag = False
                break



    index = wordIndexDict[outputWord]

    return outputWord, index

def getRandomWords(numRand: int, forbidden: list[str] = []):
    '''
    Takes in `numRand`, an optional list of forbidden words, and a `wiggleValue`. \n
    The `wiggleValue` determines the number of dimensions that the words differ from each other: larger number is more difficult for the user. Legal interval: [1, 300] \n
    Returns tuple containing a numpy array that contains `numRand` distinct word vectors, and a list with the corresponding names.
    '''
    outputVec = np.empty((numRand, vectSize), dtype=np.ndarray)
    outputWords = []

    # ---
    # choose the first random word
    index = random.randint(0, numWords - 1)
    randomWord = indexWordArray[index][0]

    while (randomWord in forbidden):
        index = random.randint(0, (numWords - 1))
        randomWord = indexWordArray[index][0]

    outputWords.append(randomWord)
    outputVec[0] = matrix[index]
    forbidden.append(randomWord)

    # ---
    # now generate all the other words

    for i in range(numRand - 1):
        wiggledWord, wiggledIndex = wiggleVector(outputVec[0], forbidden)

        outputWords.append(wiggledWord)
        outputVec[i] = matrix[wiggledIndex]

        forbidden.append(wiggledWord)


    return outputVec, outputWords


def generateRandomAverage(numRandomWords: int, forbidden: list[str] = [], kAppend: int = 10):
    '''
    Takes in int `numRandomWords`, an optional list of forbidden words, and an optional int `kAppend` of extra words to generate (only the first distinct numRandomWords words are returned).\n
    Returns a list of `numRandomWords+1` distinct random words. The last word is the average of the first `numRandomWords` words.'''

    vectors, names = getRandomWords(numRandomWords, forbidden)

    forbidden.extend(names)
    stringList = []
    for i in range(numRandomWords):
        stringList.extend((names[i], "+"))
    stringList.pop()

    averageVector = wordsToVect(stringList) / numRandomWords

    arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
    arrayofVectors[0] = averageVector

    k = kAppend + numRandomWords
    indices, distances = indexNN.query(arrayofVectors, k=k)
    outputWord = "!!None!!"

    for i in range(k):
        generatedGuess = indexWordArray[indices[0][i]][0]

        if generatedGuess in forbidden:
            continue
        else:
            outputWord = generatedGuess
            break

    names.append(outputWord)

    return names


#Some anecdotal evidence for checkAverage:
#   kAppend == 10 has >90% false negatives, kAppend == 20 has ~5% false negatives
#   I am using kAppend == 100 to hopefully bring that number to 0, with the risk of significant false positives.
def checkAverage(wordList: list[str], kAppend: int = 10):
    '''Takes in a list of 2 or more words, and an optional integer `kAppend` denoting `kAppend` extra words to generate.\n
    Returns a boolean representing whether the last word in the list is the average of the rest.\n
    (Generates `wordList.length + kAAppend - 1` possible averages: if the last word matches any of these, returns true)
    '''
    possibleAverage = wordList.pop()
    wordListLen = len(wordList)

    stringList = []
    for word in wordList:
        stringList.extend((word, "+"))
    stringList.pop()

    averageVector = wordsToVect(stringList) / wordListLen

    arrayofVectors = np.empty((1, vectSize), dtype=np.ndarray)
    arrayofVectors[0] = averageVector

    k = kAppend + wordListLen - 1
    indices, distances = indexNN.query(arrayofVectors, k=k)

    for i in range(k):
        generatedGuess = indexWordArray[indices[0][i]][0]

        if generatedGuess == possibleAverage:
            return True

    return False

def generateSimDiff(numRandomWords: int, forbidden: list[str] = [], kAppend: int = 10):
    '''Outputs `numRandomWords + 1` length list.\n
    List contains `numRandomWords` similar words and the last is a dissimilar (random) word.'''

    simVectors, simNames = getRandomWords(numRandomWords, forbidden)
    forbidden.extend(simNames)
    diffVector, diffNames = getRandomWords(1, forbidden)

    simNames.extend(diffNames)

    return simNames

def checkSimDiff(wordList: list[str]):
    # possibleDiff = wordList.pop()
    sampleMatrix = np.empty((len(wordList), vectSize))

    for i in range(len(wordList)):
        word = wordList[i]
        vectPart = matrix[wordIndexDict[word]]
        sampleMatrix[i] = vectPart

    # test = np.array(sampleMatrix)

    distMatrix = squareform(pdist(sampleMatrix))

    possibleDiffScore = sum(distMatrix[-1])

    maximumScore = possibleDiffScore
    for i in range(len(distMatrix)):
        maximumScore = max(maximumScore, sum(distMatrix[i]))

    return bool(possibleDiffScore == maximumScore)
















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


