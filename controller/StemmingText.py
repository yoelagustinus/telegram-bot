# import StemmerFactory from Sastrawi
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# function Stemming Text
def stemmingText(txt):
	# create stemmer
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()

	# proses stemming
	result = stemmer.stem(txt)

	return result