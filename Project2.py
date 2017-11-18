##################################################
#                  -- PROJECT 2 --               #
#                   COMP 4980-04                 #
#                 FRANCESCA RAMUNNO              #
#               AND MONIKA PIECHATZEK            #
##################################################

import nltk as nltk
from nltk import *

# -- THINGS TO COUNT -- #
# 1) EMOTION WORD, ALONE, NOT PRECEDED BY VALENCY SHIFTER
# 2) EMOTION WORD IN A BIGRAM, PRECEDED BY ONE OR TWO NEGATION WORDS
# 3) EMOTION WORD IN A TRIGRAM