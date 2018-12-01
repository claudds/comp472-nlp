from collections import Counter
from math import log10
import re

def readFileTrain(filename):
    with open(filename, 'r') as file:
        #read in the whole file
        data = file.read()
        data = re.sub(r'[^a-z ]','',data)
    return data.lower()

def readFileTest(filename):
    testSentences = []
    with open(filename, 'r') as file:
        #read in the whole file
        testSentences = [line for line in file.read().split('\n')]
    return testSentences


def unigramTrain(text, characters, outputFile, smoothing):
    text = text.replace(' ','')
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

def bigramTrain(text, characters, outputFile, smoothing):
    pairs = {}
    letters = {}
    for c1 in characters:
        letters[c1]=0
        pairs[c1]={}
        for c2 in characters:
            pairs[c1][c2]=0
    
    for i in range(0, len(text)-1):
        if(text[i]==' ' or text[i+1]==' '):
            continue
        pairs[text[i]][text[i+1]]+=1
        letters[text[i]]+=1
    probabilities = {}

    for p1 in pairs.keys():
        probabilities[p1]={}
        for p2 in pairs[p1].keys():
            probabilities[p1][p2] = (pairs[p1][p2]+smoothing)/(smoothing*len(letters)+letters[p1])
    
    with open(outputFile, 'w') as file:
        for p1 in probabilities.keys():
            for p2 in probabilities[p1].keys():
                file.write("P(" + p2 + " | " + p1 + " ) = " + str(probabilities[p1][p2]) + '\n')
    
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

    testString = re.sub(r'[^a-z ]','',testString)

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

def bigramTest(frModel, enModel, itModel, testString, filename):
    probEn = (2/6)
    probFr = (2/6)
    probIt = (2/6)

    testDict = {}
    testDict["English"] = log10(probEn)
    testDict["French"] = log10(probFr)
    testDict["Italian"] = log10(probIt)
    
    testString = testString.lower()
    testString = re.sub(r'[^a-z ]','',testString)

    with open(filename, 'a') as file:
        file.write("\n---------------- \n")
        for i in range(0, len(testString)-1):
            if(testString[i]==' ' or testString[i+1]==' '):
                continue
            enProb = log10(enModel[testString[i]][testString[i+1]])
            frProb = log10(frModel[testString[i]][testString[i+1]])
            itProb = log10(itModel[testString[i]][testString[i+1]])

            file.write("\nBigram: " + testString[i]+testString[i+1] + "\n")
            testDict["English"] += enProb
            testDict["French"] += frProb
            testDict["Italian"] += itProb

            file.write("English: P(" + testString[i+1] + "|" + testString[i] + ") =" + str(enProb) + " ==> log prob of sentence so far: " + str(testDict["English"]) + "\n")
            file.write("French: P(" + testString[i+1] + "|" + testString[i] + ") =" + str(frProb) + " ==> log prob of sentence so far: " + str(testDict["French"])+ "\n")
            file.write("Italian: P(" + testString[i+1] + "|" + testString[i] + ") =" + str(itProb) + " ==> log prob of sentence so far: " + str(testDict["Italian"])+ "\n")
       
    maxProb = max(testDict, key=testDict.get)
    with open(filename, 'a') as file:
        file.write("\nAccording to the unigram model, the sentence is in " + maxProb)
    return maxProb

characters = list(readFileTrain("train/character-set.txt"))
testSentences = readFileTest("test/test-sentences.txt")

## English training
textE1 = readFileTrain("train/en-moby-dick.txt")
textE2 = readFileTrain("train/en-the-little-prince.txt")
trainingText = textE1 + " " + textE2
enUnigramModel = unigramTrain(trainingText, characters, "models/unigramEN.txt", 0.5)
enBigramModel = bigramTrain(trainingText, characters, "models/bigramEN.txt", 0.5)

## French Training
textF1 = readFileTrain("train/fr-le-petit-prince.txt")
textF2 = readFileTrain("train/fr-vingt-mille-lieues-sous-les-mers.txt")
trainingText = textF1 + " " + textF2
frUnigramModel = unigramTrain(trainingText, characters, "models/unigramFR.txt", 0.5)
frBigramModel = bigramTrain(trainingText, characters, "models/bigramFR.txt", 0.5)


## Italian Training
textI1 = readFileTrain("train/it-il-trono-di-spade.txt")
textI2 = readFileTrain("train/it-la-divina-commedia.txt")
trainingText = textI1 + " " + textI2
itUnigramModel = unigramTrain(trainingText, characters, "models/unigramOT.txt", 0.5)
itBigramModel = bigramTrain(trainingText, characters, "models/bigramOT.txt", 0.5)

counter = 1
for sentence in testSentences:
    filename = "output/out" + str(counter) + ".txt" 
    unigramResult = unigramTest(frUnigramModel, enUnigramModel, itUnigramModel, sentence, filename)
    bigramResult = bigramTest(frBigramModel, enBigramModel, itBigramModel, sentence, filename)
    print("According to the unigram model, the sentence is in " + unigramResult)
    print("According to the bigram model, the sentence is in " + bigramResult+'\n')
    counter += 1
