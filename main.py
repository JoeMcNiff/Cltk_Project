import cltk
import os
import string

from cltk.data.fetch import FetchCorpus
corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus("lat_models_cltk")
from cltk.text.lat import replace_jv
from cltk.tokenizers.lat.lat import LatinWordTokenizer
from word_counting import cltkTool

latin_file = open("Ecologue.txt")
data = latin_file.read()
latin_file.close()

test = cltkTool(data)

print(test.textTop1000())
tokenizer = LatinWordTokenizer()


#print(cltk.alphabet.lat.remove_accents("trēs") == ("trēs"))
#print("ē" == "ē")

#print(test.notTop1000List())





