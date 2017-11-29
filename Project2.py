##################################################
#                  -- PROJECT 2 --               #
#                   COMP 4980-04                 #
#                 FRANCESCA RAMUNNO              #
#               AND MONIKA PIECHATZEK            #
##################################################

# Good site for intensifiers: https://lognlearn.jimdo.com/grammar-tips/adverbs/intensifiers-adverbs-of-degree/
import nltk as nltk
import math
from nltk import *
import os
from nltk.util import ngrams
from collections import Counter
import json
import prettytable

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
# Both weak and strong intensifiers
both_int = ['little', 'hardly', 'less', 'nearly', 'almost', 'barely','very', 'extremely', 'really', 'exceptionally', 'totally', 'utterly', 'completely']
# Dict of two novels
novels = {}
novel_name = ""
# Mix of weak intensifiers, strong intensifiers and negation words. Needed for emotional_strength count
ints_and_neg_words = ['no', 'not', 'none', 'nobody', 'nothing', 'neither', 'nowhere', 'never', 'little', 'hardly', 'less', 'nearly', 'almost', 'barely','very', 'extremely', 'really', 'exceptionally', 'totally', 'utterly', 'completely']

tri = []
single = 0
bigrams = 0
trigram = 0
all_emo_words = 0
emotional_strength = 0.0

# Input for the L8 directory
def directory_input(message):
    path = input(message)
    if os.path.isdir(path):
        return path
    else:
        return directory_input('Enter an existing directory path or quit (ctrl+C): ')

# Makes a trigram out of the novel only
novel_root = directory_input("Please enter a novel directory: ")
print("")
root="tmp"

novel_names = []

for subdir, dirs, files in os.walk(novel_root):
    for file in files:
        print("Filtering " + file + " and finding bigrams....")
        print("")
        novel_name = file
        novel_names.append(novel_name)
        novels[file] = {}
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
        # Stack of the novel to be popped
        novel_pop = []


        # For some reason the tuples were getting deleted, however when copied over
        # to a new_novel, they weren't getting deleted and thats why I have This
        # new_novel which holds the trigrams of the novel
        for sent in tri:
            for tup in sent:
                holding.append(tup)
                novel_pop.append(tup)
            new_novel.append(holding)
            holding = []


        # Gets the L8 Words, only asks once
        if root == "tmp":
            root = directory_input("Please enter a directory path for the 8 texts: ")

        for subdir, dirs, files in os.walk(root):
            for file in files:
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
                        # Finds WORD regardless of what is in front of it
                        if tup[2] in emo_words_list[emotion]:
                            # Finds WORD, so 'lonley single emotion words'. Taking into consideration of whats infront of it (NO NEGATION WORDS).
                            if tup[0] not in neg_words and tup[1] not in neg_words:
                                big_dict[emotion] += 1
                                # print("single:",tup, "for EMOTION:",emotion)
                            # Finds NEG EMO
                            if tup[1] in neg_words and tup[0] not in neg_words:
                                big_dict["no "+ emotion] +=1
                                # print("NEG EMO:", tup, "for EMOTION: no",emotion)
                            # Finds NEG NEG EMO
                            if tup[0] in neg_words and tup[1] in neg_words:
                                big_dict["no "+ emotion] +=1
                                # print("NEG NEG EMO:",tup, "for EMOTION: no",emotion)
                            # FINDS NEG STRON_INT WORD which would be 'negative' (ie. I am not very happy)
                            # Not truley negative because it will also count (ie. I am not very sad)
                            # NEG x STRONG_INT(POS)= NEG
                            if tup[1] in str_int and tup[0] in neg_words:
                                big_dict["no "+ emotion] +=1
                                # print("NEG STR_INT EMO:",tup, "for EMOTION: no",emotion)
                            # Finds NEG WEAK_INT WORD which would be 'positive' (ie. I am no less happy)
                            #  NEG x WEAK_INT(NEG) = POS
                            if tup[1] in w_int and tup[0] in neg_words:
                                big_dict[emotion] +=1

                # Loops through novel of tuples and removes them from novel_pop once filtered through to avoid dupication.
                for tup in novel_pop:
                    # Finds WORD regardless of what is in front of it
                    if tup[2] in emo_words_list[emotion]:
                        all_emo_words +=1
                        # Finds WORD, so 'lonley single emotion words'. Taking into consideration of whats infront of it (NO NEGATION WORDS).
                        if tup[0] not in neg_words and tup[1] not in neg_words:
                            single += 1
                            # print("single:",tup, "for EMOTION:",emotion)
                        # Finds NEG EMO
                        if tup[1] in neg_words and tup[0] not in neg_words:
                            bigrams += 1
                            # print("NEG EMO:", tup, "for EMOTION: no",emotion)
                        # Finds NEG NEG EMO
                        if tup[0] in neg_words and tup[1] in neg_words:
                            trigram += 1
                            # print("NEG NEG EMO:",tup, "for EMOTION: no",emotion)
                        # FINDS NEG STRONG_INT WORD which would be 'negative' (ie. I am not very happy)
                        # (Not truley negative because it will also count (ie. I am not very sad))
                        # NEG x STRONG_INT(POS)= NEG
                        if tup[1] in str_int and tup[0] in neg_words:
                            trigram += 1
                            # print("NEG STR_INT EMO:",tup, "for EMOTION: no",emotion)
                        # Finds NEG WEAK_INT WORD which would be 'positive' (ie. I am no less happy)
                        # NEG x WEAK_INT(NEG) = POS
                        if tup[1] in w_int and tup[0] in neg_words:
                            trigram +=1
                            # print("NE W_INT EMO:",tup, "for EMOTION:",emotion)
                        # Counts emotional strength: finds BLANK STR_INT EMO, so just emo word with strong intensifier, without negation word in front.
                        if tup[0] not in neg_words and tup[1] in str_int:
                            emotional_strength += 1.5
                            # print("BLANK STR_INT EMO:",tup, "for EMOTION:",emotion)
                        # Counts emotional strength: find BLANK W_INT EMO, so just emo word with weak intensifier and without negation word in front.
                        if tup[0] not in neg_words and tup[1] in w_int:
                            emotional_strength += 0.5
                            # print("BLANK W_INT EMO:",tup, "for EMOTION:",emotion)
                        # Counts emotional strength: finds BLANK BLANK EMO, so just the lonley emo word without intensifiers or negation words in front.
                        if tup[0] not in neg_words and tup[1] not in ints_and_neg_words:
                            emotional_strength += 1.0
                            # print("BLANK BLANK EMO:",tup, "for EMOTION:",emotion)
                        # Removes tuple from the novel so there will be no duplicate counts (ie. 'I am happy' could be both joy and trust)
                        novel_pop.remove(tup)
            print("")
            print("Information found: ")
            print("")
            print("Token count:",len(token))
            print("Sentence count:",len(sent_toke))
            print("")

            percent_em_exp = (all_emo_words / len(token)) * 100

            to_print = [novel_name,all_emo_words,bigrams,trigram,emotional_strength,percent_em_exp]
            tbl = prettytable.PrettyTable(
                ["Novel", "# emotional words-unigram", "# emotional words-bigram", "# emotional words-trigram",
                 "Emotional Strength","% emotional expressions"])
            tbl.add_row(to_print)
            print(tbl)
            all_emo_words = 0
            bigrams = 0
            trigram = 0
            emotional_strength = 0
            print("")
        # Saves each novels 16 word count
        novels[novel_name] = big_dict

print("")
print("-- ANALYSIS OF THESE FINDINGS --")
print("")

# -- build a table -- #
head = [k for k in novels]
head.insert(0,"Emotion")
emotions = []
to_print = []
for k,v in novels.items():
    for k1,v1 in v.items():
        if k1 not in emotions:
            emotions.append(k1)
            to_print.append([k1])
        for val in to_print:
            if val[0] == k1:
                val.append(v1)

pos = ["joy","trust"]
neg = ["disgust","fear","anger","sadness"]
neut = ["anticipation", "surprise"]

txt1_pos_count = 0
txt1_neg_count = 0
txt1_neut_count = 0

txt2_pos_count = 0
txt2_neg_count = 0
txt2_neut_count = 0

op_tbl = prettytable.PrettyTable(head)
for arr in to_print:
    op_tbl.add_row(arr)
    if arr[0] in pos:
        txt1_pos_count = txt1_pos_count + arr[1]
        txt2_pos_count = txt2_pos_count + arr[2]
    if arr[0] in neg:
        txt1_neg_count = txt1_neg_count + arr[1]
        txt2_neg_count = txt2_neg_count + arr[2]
    if arr[0] in neut:
        txt1_neut_count = txt1_neut_count + arr[1]
        txt2_neut_count = txt2_neut_count + arr[2]

print("")
print("EMOTION COUNTS COMPARISON BETWEEN NOVELS:")
print("")
print(op_tbl)

# -- make lists for each novel of negativity, positivity, neutrality -- #
novel1 = [novel_names[0], txt1_neg_count, txt1_pos_count, txt1_neut_count]
novel2 = [novel_names[1], txt2_neg_count, txt2_pos_count, txt2_neut_count]

print("")
print("POSITIVITY, NEGATIVITY, NEUTRALITY IN THESE NOVELS:")
print("")

# -- put em in a table! -- #
pnn_table = prettytable.PrettyTable(["Novel","Negativity","Positivity","Neutrality"])
pnn_table.add_row(novel1)
pnn_table.add_row(novel2)
print(pnn_table)
print("")

if abs(novel1[1] - novel2[1]) < 50:
    print("These novels have similar negativity.")
else:
    if novel1[1] > novel2[1]:
        print(novel_names[0], "is more negative than", novel_names[1])
    else:
        print(novel_names[1], "is more negative than", novel_names[0])

if abs(novel1[2] - novel2[2]) < 50:
    print("These novels have similar positivity.")
else:
    if novel1[2] > novel2[2]:
        print(novel_names[0], "is more positive than", novel_names[1])
    else:
        print(novel_names[0], "is more positive than", novel_names[0])

if abs(novel1[3] - novel2[3]) < 50:
    print("These novels have similar neutrality.")
else:
    if novel1[3] > novel2[3]:
        print(novel_names[0], "is more neutral than", novel_names[1])
    else:
        print(novel_names[1], "is more neutral than", novel_names[0])




