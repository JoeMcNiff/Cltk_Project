import os
import cltk
import string
import unittest
from unittest.mock import patch

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.tokenizers.lat.utils import LatinSentenceTokenizerTrainer
from cltk.tokenizers.line import LineTokenizer
from cltk.tokenizers.word import WordTokenizer

#from cltk.data.fetch import FetchCorpus
from cltk.lemmatize.backoff import (
    DefaultLemmatizer,
    DictLemmatizer,
    IdentityLemmatizer,
    RegexpLemmatizer,
    UnigramLemmatizer,
)
from cltk.lemmatize.lat import LatinBackoffLemmatizer, RomanNumeralLemmatizer
from cltk.text.lat import replace_jv
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from cltk.utils import CLTK_DATA_DIR

class cltkTool(unittest.TestCase):

  @classmethod
  def __init__(self, latin_text):
    # Clean up the latin_text
    latin_text = latin_text.translate(str.maketrans('', '', string.punctuation))
    latin_text = replace_jv(latin_text)
    latin_text = latin_text.lower()
    latin_text = cltk.alphabet.lat.remove_macrons(latin_text)
    self.latin_text = latin_text
    
    self.tokens = self.word_tokenizer_latin(self)
    
    self.lemmas = self.lemma(self, self.tokens)
    # Creates top1000 list
    top1000File = open("top_1000.txt", "r")
    self.top1000 = top1000File.readlines()
    top1000File.close()
    # Creates frequency rank list
    freqRankFile = open("frequency_ranks.txt", "r")
    self.frequency_ranks = freqRankFile.readlines()
    freqRankFile.close()

    # Create a dictionary with the word as the keyvalue and the number of appearances as the corresponding entry
    wordAppearances = {}
    for lemma in self.lemmas:
        word = lemma[1]
        if "1" in lemma[1]:
          word = word.replace("1", "")
        if "2" in lemma[1]:
          word = word.replace("2", "")
        if word in wordAppearances:
          wordAppearances[word] += 1
        else:
          wordAppearances[word] = 1
    self.wordAppearances = wordAppearances

  def word_tokenizer_latin(self):
    #target = self.latin_text
    tokenizer = LatinWordTokenizer()
    tokenized_words = tokenizer.tokenize(self.latin_text)

    return tokenized_words

  def unique_Word_Counter(self, tokens):
    checked = []
    num_Unique = 0
    for word in tokens:
      if (word[1] not in checked):
        checked.append(word[1])
        num_Unique += 1

    return num_Unique

  def num_Unique(self):
    tokens = self.word_tokenizer_latin()
    lemmas = self.lemma(tokens)

    return self.unique_Word_Counter(lemmas)

  def lemma(self, tokens):
    lemmatizer = LatinBackoffLemmatizer()
    tokens = lemmatizer.lemmatize(tokens)
    return tokens

  def inTop1000(self, word):  
    word += "\n"
    if word in self.top1000:
      return True
    else:
      return False

  # Returns the percentage in top1000 and gives the frequency rank of each word in the output file ("---" for words not in top1000)
  def textTop1000(self):

    file3 = open("output.txt", "w")
    file3.write("List of words in the text with their # of appearances followed by their respective frequency rank if they are top1000:\n\n")

    lemmas = self.lemmas
    num1000 = 0.0
    for lemma in lemmas:
        word = lemma[1]
        if "1" in lemma[1]:
          word = word.replace("1", "")
        if "2" in lemma[1]:
          word = word.replace("2", "")
        
        if self.inTop1000(word):
            num1000 += 1
            file3.write(self.top1000[self.top1000.index(word+"\n")].strip() + ", " + str(self.wordAppearances[word])+ " appearances, rank: "+ self.frequency_ranks[self.top1000.index(word+"\n")])
        else:
          # This is here for if you are examinging vocab lists for chapters.
          if "capitul" in lemma[1]:
            file3.write("\n")

          file3.write(word.strip() + ", "+str(self.wordAppearances[word])+ " appearances, rank: "+"---\n")



    file3.close()    
    return num1000/len(lemmas)  

  # Creates a list of unique latin words in the text that are not top1000      
  def notTop1000List(self):
    lemmas = self.lemmas
    list = []
    for lemma in lemmas:
      if not self.inTop1000(lemma[1]) and lemma[1] not in list:
        list.append(lemma[1])
    
    return list

    
    
    

    



