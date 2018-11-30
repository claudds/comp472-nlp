import string
from collections import Counter
from math import log10

punct = str.maketrans('', '', string.punctuation)
digits = str.maketrans('', '', string.digits)
def readFileTrain(filename):
    with open(filename, 'r') as file:
        #read in the whole file
        data = file.read()
        data = ''.join(data.split())
        data = data.translate(punct)
        data = data.translate(digits)
    return data.lower()

def readFileTest(filename):
    testSentences = []
    with open(filename, 'r') as file:
        #read in the whole file
        testSentences = [line for line in file.read().split('\n')]
    return testSentences


def unigramTrain(text, characters, outputFile, smoothing):
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
        pairs[text[i]][text[i+1]]+=1
        letters[text[i]]+=1
    probabilities = {}

    for p1 in pairs.keys():
        probabilities[p1]={}
        for p2 in pairs[p1].keys():
            probabilities[p1][p2] = (pairs[p1][p2]+smoothing)/(smoothing*letters[p1]+letters[p1])
    
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

    testString = testString.translate(punct)
    testString = testString.translate(digits)

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
    return ""

characters = list(readFileTrain("train/character-set.txt"))
testSentences = readFileTest("test/test-sentences.txt")

## English training
textE1 = readFileTrain("train/en-moby-dick.txt")
textE2 = readFileTrain("train/en-the-little-prince.txt")
trainingText = str(textE1 + textE2)
enBigramModel = bigramTrain(trainingText, characters, "models/bigramEN.txt", 0.5)
# enUnigramModel = unigramTrain(trainingText, characters, "models/unigramEN.txt", 0.5)
# enBigramModel = bigramTrain(trainingText, characters, "", 0)


# ## French Training
# textF1 = readFileTrain("train/fr-le-petit-prince.txt")
# textF2 = readFileTrain("train/fr-vingt-mille-lieues-sous-les-mers.txt")
# trainingText = textF1 + textF2
# frUnigramModel = unigramTrain(trainingText, characters, "models/unigramFR.txt", 0.5)
# frBigramModel = bigramTrain(trainingText, characters, "", 0)


# ## Italian Training
# textI1 = readFileTrain("train/it-il-trono-di-spade.txt")
# textI2 = readFileTrain("train/it-la-divina-commedia.txt")
# trainingText = textI1 + textI2
# itUnigramModel = unigramTrain(trainingText, characters, "models/unigramOT.txt", 0.5)
# frBigramModel = bigramTrain(trainingText, characters, "", 0)

# counter = 1
# for sentence in testSentences:
#     filename = "output/out" + str(counter) + ".txt" 
#     unigramResult = unigramTest(frUnigramModel, enUnigramModel, itUnigramModel, sentence, filename)
#     print("According to the unigram model, the sentence is in " + unigramResult)
#     counter += 1
