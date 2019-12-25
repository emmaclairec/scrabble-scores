from tabulate import tabulate
import pandas as pd
import numpy as np


class ScrabbleData:
    SCRAB_SCORE = {"E": 1, "A": 1, "O": 1, "T": 1, "I": 1,
                   "N": 1, "R": 1, "S": 1, "L": 1, "U": 1,
                   "D": 2, "G": 2,
                   "C": 3, "M": 3, "B": 3, "P": 3,
                   "H": 4, "F": 4, "W": 4, "Y": 4, "V": 4,
                   "K": 5,
                   "J": 8, "X": 8,
                   "Q": 10, "Z": 10}

    SCRAB_TILES = {"E": 24, "A": 16, "O": 15, "T": 15, "I": 13,
                   "N": 13, "R": 13, "S": 10, "L": 7, "U": 7,
                   "D": 8, "G": 5,
                   "C": 6, "M": 6, "B": 4, "P": 4,
                   "H": 5, "F": 4, "W": 4, "Y": 4, "V": 3,
                   "K": 2,
                   "J": 2, "X": 2,
                   "Q": 2, "Z": 2,
                   " ": 4}

    DICT_TXT = 'collinsScrabbleWords2019.txt'

    def __init__(self, word):
        self.word = word
        self.dict = self.getScrabDict()
        results = self.calcs()
        self.score = results[0]
        self.possible = results[1]
        self.viable = self.isViableWord()

    def calcs(self):
        possible = True
        blank_count = 0
        score = 0
        letter_count_dict = {}
        for letter in self.word:
            while possible:
                if blank_count > 4:
                    possible = False
                break
            if letter not in letter_count_dict:
                score += self.SCRAB_SCORE[letter]
                letter_count_dict[letter] = 1
            elif letter_count_dict[letter] <= self.SCRAB_TILES[letter]:
                score += self.SCRAB_SCORE[letter]
                letter_count_dict[letter] += 1
            else:
                blank_count += 1
        return [score, possible]

    def getScrabDict(self):
        txt = open(self.DICT_TXT, 'r').read()
        upper_txt = txt.upper()
        dict_list = upper_txt.split("\n")
        dict_list.remove("")
        dict_list.remove("Collins Scrabble Words (2019). 279,496 words. Words only.".upper())
        return dict_list

    def isViableWord(self):
        if self.word in self.dict:
            return True
        return False


class Script:

    def __init__(self, text_file):
        self.imported_text_file = text_file
        output = self.clean_text()
        self.word_list = output[0]
        self.word_count = output[1]

    def clean_text(self):
        txt = open(self.imported_text_file, 'r').read()
        upper_txt = txt.upper()
        remove = ".,!?:0123456789" + '"' + '\n'
        trans_dict = upper_txt.maketrans(remove, len(remove) * " ")
        clean_txt = upper_txt.translate(trans_dict)
        clean_txt = clean_txt.replace("'", "")
        clean_txt = clean_txt.replace("-", "")
        txt_list = clean_txt.split(" ")
        txt_set = set(txt_list)
        txt_set.remove('')
        word_count = {}
        for item in txt_list:
            if item in txt_set:
                if item in word_count:
                    word_count[item] += 1
                else:
                    word_count[item] = 1
        txt_final = list(txt_set)
        txt_final.sort()
        return [txt_final, word_count]


bee_movie = Script('beeMovieScript.txt')


df = []
for word in bee_movie.word_list:
    word_info = ScrabbleData(word)
    df.append([word, bee_movie.word_count[word], word_info.score,
               ['Yes' if word_info.possible else 'No'], ['Yes' if word_info.viable else 'No']])
resultsTable = pd.DataFrame(df, columns=['Word', 'Times Repeated', 'Score', 'Possible', 'Official Scrabble Word'])
resultsTable.set_index('Word', drop=True, inplace=True)

print(tabulate(["ALL RESULTS BY SCORE"], tablefmt='fancy_grid'))
print(tabulate(resultsTable.sort_values(['Score'], ascending=False), headers='keys', showindex=True,
               tablefmt="fancy_grid"))

print(tabulate(["INT SUMMARIES"], tablefmt='fancy_grid'))
print(tabulate(resultsTable.describe(include=[np.number]), headers='keys', showindex=True,
               tablefmt="fancy_grid"))


def fix_ind(df, header, table_name):
    df.reset_index(inplace=True)
    for index, row in df.iterrows():
        if row[0] == ['Yes']:
            df.loc[index, 'index'] = 'Yes'
        else:
            df.loc[index, 'index'] = 'No'
        if header == '%':
            df.loc[index, '%'] = round(df.loc[index, '%'] * 100, 2)
    df.columns = [table_name, header]
    df.set_index(table_name, inplace=True)
    return df


print(tabulate(["POSSIBLE WORD STATS"], tablefmt='fancy_grid'))
poss = resultsTable['Possible'].value_counts()
poss_df = poss.to_frame(name='Count')
poss_df = fix_ind(poss_df, 'Count', 'POSSIBLE')
poss_norm = resultsTable['Possible'].value_counts(normalize=True)
poss_norm_df = poss_norm.to_frame(name='%')
poss_norm_df = fix_ind(poss_norm_df, '%', 'POSSIBLE')
poss_df.join(poss_norm_df)
print(tabulate(poss_df, headers='keys', showindex=True, tablefmt='fancy_grid'))


print(tabulate(["OFFICIAL WORD STATS"], tablefmt='fancy_grid'))
ofw = resultsTable['Official Scrabble Word'].value_counts()
ofw_df = ofw.to_frame(name='Count')
ofw_df = fix_ind(ofw_df, 'Count', 'OFFICIAL')
ofw_norm = resultsTable['Official Scrabble Word'].value_counts(normalize=True)
ofw_norm_df = ofw_norm.to_frame(name='%')
ofw_norm_df = fix_ind(ofw_norm_df, '%', 'OFFICIAL')
ofw_df.join(ofw_norm_df)
print(tabulate(ofw_df, headers='keys', showindex=True, tablefmt='fancy_grid'))


