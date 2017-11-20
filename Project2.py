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

# Input for the L8 directory
def directory_input(message):
    path = input(message)
    if os.path.isdir(path):
        return path
    else:
        return directory_input('Enter an existing directory path or quit (ctrl+C): ')

root = directory_input("Please enter a directory path for the 8 texts: ")
for subdir, dirs, files in os.walk(root):
    for file in files:
        print("Filtering " + file + " and finding bigrams....")

        # prints out the words in the L8 files
        filez = open(root+"/"+file, "r")
        for line in filez:
            print(line)
            print(file)
