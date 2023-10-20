import nltk
import string
import re
from autocorrect import Speller

class Preprocessing:
    def __init__(self,testo):
        self.testo = testo 

    def get_tokens(self):
        return self.tokens
    
    def get_text(self):
        return self.testo
    
    #step 1 tokenizzazione: dividere il testo in parole individuali(token)
    def tokenizzazione(self):
        self.tokens = nltk.word_tokenize(self.testo)
        
    
    #step 2 lowercasing : rendere le maiuscole minuscole 
    def lowercasing(self):
        self.tokens = [token.lower() for token in self.tokens]

    #step 3 remove punctuation
    def remove_punctuation(self):
        self.tokens = [token for token in self.tokens if token not in string.punctuation]
    
    #step 4 remove punctuationstopwords in italian (es il e ecc..)
    def remove_stopword(self):
        stopwords = nltk.corpus.stopwords.words("italian")
        self.tokens = [token for token in self.tokens if token.lower() not in stopwords]

    #step 5 remove whitespace: replace multiple consecutive white space characters with a single space
    def remove_whitespace(self):
        self.testo = self.testo.strip()
        self.testo = " ".join(self.testo.split())
    
    #step 6 remove url 
    def remove_url(self):
        pattern = r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
        #replace URLs with an empty string
        self.testo = re.sub(pattern, " ", self.testo)
      

    #step 7 spelling correction
    def spelling_correction(self):
        # Crea un oggetto Speller per la lingua italiana
        spell = Speller(lang='it')
        correzioni = [spell(token) for token in self.tokens]
        self.tokens = correzioni
        # Unisci le parole corrette in un testo corretto
        self.testo = ' '.join(correzioni)
        