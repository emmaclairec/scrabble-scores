import pandas as pd

scrabScore = {"E" : 1, "A" : 1, "O" : 1, "T" : 1, "I" : 1,\
              "N" : 1, "R" : 1, "S" : 1, "L" : 1, "U" : 1,\
              "D" : 2, "G" : 2,\
              "C" : 3, "M" : 3, "B" : 3, "P" : 3,\
              "H" : 4, "F" : 4, "W" : 4, "Y" : 4, "V" : 4,\
              "K" : 5,\
              "J" : 8, "X" : 8,\
              "Q" : 10, "Z" : 10}

scrabTiles = {"E" : 24, "A" : 16, "O" : 15, "T" : 15, "I" : 13,\
              "N" : 13, "R" : 13, "S" : 10, "L" : 7, "U" : 7,\
              "D" : 8, "G" : 5,\
              "C" : 6, "M" : 6, "B" : 4, "P" : 4,\
              "H" : 5, "F" : 4, "W" : 4, "Y" : 4, "V" : 3,\
              "K" : 2,\
              "J" : 2, "X" : 2,\
              "Q" : 2, "Z" : 2,\
              " " : 4}


def isValidWord(word):
    blankCount = 0
    letterCountDict = {}
    for letter in word:
        if letter not in letterCountDict:
            letterCountDict[letter] = 1
        else:
            letterCountDict[letter] = letterCountDict[letter] + 1

    for letter in letterCountDict:
        if letterCountDict[letter] > scrabTiles[letter]:
            blankCount = blankCount + letterCountDict[letter] - scrabTiles[letter]
            if blankCount > 4:
                return False
    return True


def calcScore(word):
    score = 0
    letterCountDict = {}

    for letter in word:
        score = score + scrabScore[letter]
        if letter not in letterCountDict:
            letterCountDict[letter] = 1
        else:
            letterCountDict[letter] = letterCountDict[letter] + 1

    for letter in letterCountDict:
        if letterCountDict[letter] > scrabTiles[letter]:
            score = score - ((letterCountDict[letter] - scrabTiles[letter]) * scrabScore[letter])
    return score

def removeDuplicates(list):
    finalscript = []
    seen = set()
    for word in list:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if word not in seen:
            finalscript.append(word)
            seen.add(word)
    return finalscript

with open('beeMovieScript.txt', 'r') as f:
    script = f.read()
    script = script.upper()
    transtring = ".,-!?:0123456789"+'"'+'\n'
    table = script.maketrans(transtring,len(transtring)*" ")
    newscript = script.translate(table)
    newscript = newscript.replace("'","")
    newscript = newscript.split(" ")
    newscript = list(filter(None, newscript))


finalScript = removeDuplicates(newscript)


resultsTable = pd.DataFrame(data = {'Word': [word for word in finalScript],\
                                      'Score': [calcScore(word) for word in finalScript],\
                                      'Valid': [isValidWord(word) for word in finalScript]})
resultsTable.sort_values(['Score'],ascending=False)
