##################################################
#                  -- PROJECT 2 --               #
#                   COMP 4980-04                 #
#                 FRANCESCA RAMUNNO              #
#               AND MONIKA PIECHATZEK            #
##################################################
# Good site for intensifiers: https://lognlearn.jimdo.com/grammar-tips/adverbs/intensifiers-adverbs-of-degree/
import nltk as nltk
from nltk import *
import os
from nltk.util import ngrams
from collections import Counter
import json
# -- THINGS TO COUNT -- #
# 1) EMOTION WORD, ALONE, NOT PRECEDED BY VALENCY SHIFTER
# 2) EMOTION WORD IN A BIGRAM, PRECEDED BY ONE OR TWO NEGATION WORDS
# 3) EMOTION WORD IN A TRIGRAM

# Negation words
neg_words = ['no', 'not', 'none', 'nobody', 'nothing', 'neither', 'nowhere', 'never']
# Strong intensifiers
str_int = ['very', 'extremely', 'really', 'exceptionally', 'totally', 'utterly', 'completely']
# Weak intensifiers
w_int = ['little', 'hardly', 'less', 'nearly', 'almost', 'barely']
tri = [] # Holds the trigrams, but is discarded after first use, new_novel holds the trigrams afterwards

# Input for the L8 directory
def directory_input(message):
    path = input(message)
    if os.path.isdir(path):
        return path
    else:
        return directory_input('Enter an existing directory path or quit (ctrl+C): ')

# Makes a trigram out of the novel only
novel_root = directory_input("Please enter a novel directory: ")
for subdir, dirs, files in os.walk(novel_root):
    for file in files:
        print("Filtering " + file + " and finding bigrams....")

        # prints out the words in the L8 files
        file = open(novel_root+"/"+file).read()
        token = nltk.word_tokenize(file)
        # Organizes text into sentences
        sent_toke = nltk.sent_tokenize(file)
        # Makes the sentence clean of \n
        sent_toke = [s.replace('\n', ' ') for s in sent_toke]
        # Separates the words
        tokenized_text = [nltk.word_tokenize(t) for t in sent_toke]
        for sent in tokenized_text:
            trigrams = nltk.trigrams(sent)
            tri.append(trigrams)

# Holds our 16 word counts
big_dict = {}
# holds the list of all the txt words
emo_words_list = {}
# Holds the new trigram
new_novel = []
# helper list variable for the mini for loop below
holding = []

# For some reason the tuples were getting deleted, however when copied over
# to a new_novel, they weren't getting deleted and thats why I have This
# new_novel which holds the trigrams of the novel
for sent in tri:
    for tup in sent:
        holding.append(tup)
    new_novel.append(holding)
    holding = []


# Gets the L8 Words
root = directory_input("Please enter a directory path for the 8 texts: ")
# /Users/monikapiechatzek/Documents/SCHOOL/TRU/TRU2017/FALL2017/COMP498004/PROJECT 2/L8
for subdir, dirs, files in os.walk(root):
    for file in files:
        # print("Filtering " + file + " and finding emotional words....")

        # opens txt file and reads it
        filez = open(root+"/"+file, "r")

        # takes txt title to find out which emotion is it
        emotion = file[:-4]

        # creates empty dict that will hold the counts for the 16 emotions
        big_dict[emotion] = 0
        big_dict["no "+ emotion] = 0

        # creates a empty list dict to hold all the words in the txt
        emo_words_list[emotion] = []

        # creates a dict with lists of emo words (We might not need this step)
        for line in filez:
            emo_words_list[emotion].append(line.strip())

        # Should loop through trigrams and compares them to emotion list in big_dict
        for sent in new_novel:
            for tup in sent:
                # Counts the single emotion words
                if tup[2] in emo_words_list[emotion]:
                    big_dict[emotion] += 1



# Prints out the "single counts" only right now, next the negation words
print("big_dict: ",json.dumps(big_dict, indent=1))
