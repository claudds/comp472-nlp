import string
from collections import Counter

def readFile(filename):
    with open(filename, 'r') as file:
        #read in the whole file
        data = file.read()
        data = ''.join(data.split())
        punct = str.maketrans('', '', string.punctuation)
        digits = str.maketrans('', '', string.digits)
        data = data.translate(digits)
        data = data.translate(punct)
    return data.lower()

def unigramTrain(text, characters, outputFile, smoothing):
    probabilities = {x: '' for x in characters}
    letterCounts = Counter(text)
    numberOfChars = len(text)

    if smoothing == 0:
        for letter in probabilities:
            probabilities[letter] = letterCounts[letter]/numberOfChars
            #print("P(" + letter + ") = " + str(probabilities[letter]))

    
    with open(outputFile, 'w') as file:
        for letter in probabilities:
            file.write("P(" + letter + ") = " + str(probabilities[letter]) + '\n')
    
    return ""


characters = list(readFile("train/character-set.txt"))

## English Unigram training
textE1 = readFile("train/en-moby-dick.txt")
textE2 = readFile("train/en-the-little-prince.txt")
trainingText = textE1 + textE2
unigramTrain(trainingText, characters, "models/unigramEN.txt", 0)


## French Unigram Training
textF1 = readFile("train/fr-le-petit-prince.txt")
textF2 = readFile("train/fr-vingt-mille-lieues-sous-les-mers.txt")
trainingText = textF1 + textF2
unigramTrain(trainingText, characters, "models/unigramFR.txt", 0)


## Italian Unigram Training
textI1 = readFile("train/it-il-trono-di-spade.txt")
textI2 = readFile("train/it-la-divina-commedia.txt")
trainingText = textI1 + textI2
unigramTrain(trainingText, characters, "models/unigramOT.txt", 0)


