import string
from collections import Counter
from math import log10


def readFileTrain(filename):
    with open(filename, 'r') as file:
        #read in the whole file
        data = file.read()
        data = ''.join(data.split())
    return data.lower()

def readFileTest(filename):
    testSentences = []
    with open(filename, 'r') as file:
        #read in the whole file
        testSentences = [line for line in file.read().split('\n')]
    return testSentences


def train(text, characters, outputFile, smoothing):
    probabilities = {x: '' for x in characters}
    letterCounts = Counter(text)
    numberOfChars = len(text)

    if smoothing != 0:
        numberOfChars += (smoothing*numberOfChars)

    for letter in probabilities:
        probabilities[letter] = (letterCounts[letter]+smoothing)/numberOfChars

    with open(outputFile, 'w') as file:
        for letter in probabilities:
            file.write("P(" + letter + ") = " + str(probabilities[letter]) + '\n')
    
    return probabilities

## Probability of each language should be 2/6 since there's 2 texts for each
def unigramTest(frModel, enModel, itModel, testString, filename):
    probEn = (2/6)
    probFr = (2/6)
    probIt = (2/6)

    testDict = {}
    testDict["English"] = log10(probEn)
    testDict["French"] = log10(probFr)
    testDict["Italian"] = log10(probIt)

    with open(filename, 'w') as file:
        file.write(testString + "\n")
    testString = testString.lower()
    print(testString)

    with open(filename, 'a') as file:
        for char in testString:
            if char.isalpha():
                file.write("\nUnigram: " + char + "\n")
                testDict["English"] += log10(enModel[char])
                testDict["French"] += log10(frModel[char])
                testDict["Italian"] += log10(itModel[char])

                file.write("English: P(" + char + ") =" + str(log10(enModel[char])) + " ==> log prob of sentence so far: " + str(testDict["English"]) + "\n")
                file.write("French: P(" + char + ") =" + str(log10(frModel[char])) + " ==> log prob of sentence so far: " + str(testDict["French"])+ "\n")
                file.write("Italian: P(" + char + ") =" + str(log10(itModel[char])) + " ==> log prob of sentence so far: " + str(testDict["Italian"])+ "\n")

    maxProb = max(testDict, key=testDict.get)
    with open(filename, 'a') as file:
        file.write("\nAccording to the unigram model, the sentence is in " + maxProb)
    return maxProb

characters = list(readFileTrain("train/character-set.txt"))
testSentences = readFileTest("test/test-sentences.txt")

## English training
textE1 = readFileTrain("train/en-moby-dick.txt")
textE2 = readFileTrain("train/en-the-little-prince.txt")
trainingText = textE1 + textE2
enModel = train(trainingText, characters, "models/unigramEN.txt", 0.5)


## French Training
textF1 = readFileTrain("train/fr-le-petit-prince.txt")
textF2 = readFileTrain("train/fr-vingt-mille-lieues-sous-les-mers.txt")
trainingText = textF1 + textF2
frModel = train(trainingText, characters, "models/unigramFR.txt", 0.5)


## Italian Training
textI1 = readFileTrain("train/it-le-avventure-d-alice.txt")
textI2 = readFileTrain("train/it-la-divina-commedia.txt")
trainingText = textI1 + textI2
itModel = train(trainingText, characters, "models/unigramOT.txt", 0.5)

counter = 1
for sentence in testSentences:
    filename = "output/out" + str(counter) + ".txt" 
    unigramResult = unigramTest(frModel, enModel, itModel, sentence, filename)
    print("According to the unigram model, the sentence is in " + unigramResult)
    counter += 1
