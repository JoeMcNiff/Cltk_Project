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
    latin_text = latin_text.translate(str.maketrans('', '', string.punctuation))
    latin_text = replace_jv(latin_text)
    latin_text = latin_text.lower()
    self.latin_text = latin_text


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
    file = open("top_1000.txt", "r")
    top1000 = file.readlines()
    file.close()

    if word in top1000:
      return True
    else:
      return False
    
  def textTop1000(self):
    tokens = self.word_tokenizer_latin()
    lemmas = self.lemma(tokens)
    num1000 = 0.0

    for lemma in lemmas:
        if self.inTop1000(lemma[1]):
            num1000 += 1
            
    return num1000/len(lemmas)  
        
    
    

    



