import cltk
import os

from cltk.data.fetch import FetchCorpus
corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus("lat_models_cltk")

#from cltk.corpus.utils.importer import CorpusImporter
#my_latin_downloader = CorpusImporter('latin')
#my_latin_downloader.import_corpus('latin_text_latin_library')
#my_latin_downloader.import_corpus('latin_models_cltk')

from word_counting import cltkTool

latin_file = open("Latin.txt")
data = latin_file.read()
latin_file.close()

test = cltkTool(data)

num = test.num_Unique()
print(num)

print(test.textTop1000())


