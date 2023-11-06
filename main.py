from preprocessing import Preprocessing
from preprocessing import AnswerMe
from pdfop import PdfOp
from PyPDF2 import PdfReader
from autocorrect import Speller
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import nltk
import re
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer 
import heapq


# #nltk.download()

#TEST1 LETTURA DI UN PDF ED ESTRAZIONE DEL TESTO
#reader = PdfReader("Tracciaprogetto.pdf")
risposta = AnswerMe()
elaboratore_pdf = PdfOp("ManualePraticoJava.pdf")
numero_pagina = 22
testo_pagina = elaboratore_pdf.lettura_pagina(numero_pagina)
#if testo_pagina :
 #  print (f"pagina {numero_pagina}:\n{testo_pagina}")


#TEST2 PRE-ELABORAZIONE TESTO PAGINA PDF 
pre_elaborazione_pdf = Preprocessing(testo_pagina)
pre_elaborazione_pdf.remove_url()
pre_elaborazione_pdf.remove_whitespace()
pre_elaborazione_pdf.tokenizzazione()
#pre_elaborazione_pdf.spelling_correction()
pre_elaborazione_pdf.lowercasing()
pre_elaborazione_pdf.remove_punctuation()
pre_elaborazione_pdf.remove_stopword()
tfidf_vectors = pre_elaborazione_pdf.TFIDF(pre_elaborazione_pdf.get_tokens())

print(pre_elaborazione_pdf.get_text())

class Preprocessings:
    #constructor
    def __init__(self,txt):
        # Tokenization
        nltk.download('punkt')  #punkt is nltk tokenizer 
        # breaking text to sentences
        tokens = nltk.sent_tokenize(txt) 
        self.tokens = tokens
        self.tfidfvectoriser=TfidfVectorizer()

    # Data Cleaning
    # remove extra spaces
    # convert sentences to lower case 
    # remove stopword
    def clean_sentence(self, sentence, stopwords=False):
        sentence = sentence.lower().strip()
        sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
        if stopwords:
            sentence = remove_stopwords(sentence)
        return sentence

    # store cleaned sentences to cleaned_sentences
    def get_cleaned_sentences(self,tokens, stopwords=False):
        cleaned_sentences = []
        for line in tokens:
            cleaned = self.clean_sentence(line, stopwords)
            cleaned_sentences.append(cleaned)
        return cleaned_sentences

    #do all the cleaning
    def cleanall(self):
        cleaned_sentences = self.get_cleaned_sentences(self.tokens, stopwords=True)
        cleaned_sentences_with_stopwords = self.get_cleaned_sentences(self.tokens, stopwords=False)
        # print(cleaned_sentences)
        # print(cleaned_sentences_with_stopwords)
        return [cleaned_sentences,cleaned_sentences_with_stopwords]

    # TF-IDF Vectorizer
    def TFIDF(self,cleaned_sentences):
        self.tfidfvectoriser.fit(cleaned_sentences)
        tfidf_vectors=self.tfidfvectoriser.transform(cleaned_sentences)
        return tfidf_vectors

    #tfidf for question
    def TFIDF_Q(self,question_to_be_cleaned):
        tfidf_vectors=self.tfidfvectoriser.transform([question_to_be_cleaned])
        return tfidf_vectors

    # main call function
    def doall(self):
        cleaned_sentences, cleaned_sentences_with_stopwords = self.cleanall()
        tfidf = self.TFIDF(cleaned_sentences)
        return [cleaned_sentences,cleaned_sentences_with_stopwords,tfidf]


preprocess = Preprocessings(testo_pagina)
cleaned_sentences,cleaned_sentences_with_stopwords,tfidf_vectors = preprocess.doall()
print(cleaned_sentences)
user_question = "java per la prima volta"
#define method
method = 1
question = preprocess.clean_sentence(user_question, stopwords=True)
question_embedding = preprocess.TFIDF_Q(question)

similarity_heap = AnswerMe.RetrieveAnswer(question_embedding , tfidf_vectors ,method)
print("Question: ", user_question)

# number of relevant solutions you want here it will print 2
number_of_sentences_to_print = 1

while number_of_sentences_to_print>0 and len(similarity_heap)>0:
    x = similarity_heap.pop(0)
    print(cleaned_sentences_with_stopwords[x[1]])
    number_of_sentences_to_print-=1



# # #step 7 remove parole frequenti 
# # fdist = nltk.FreqDist(tokens)
# # # remove the most common words (e.g., the top 10% of words by frequency)
# # filtered_tokens = [token for token in tokens if fdist[token] < fdist.N() * 0.1]
# # print("Text senza parole frequenti :", filtered_tokens)

# #step 9 spelling correction
# elaboratore.spelling_correction()
# #print("Testo originale:", text)
# #print("Testo corretto:", elaboratore.testo_corretto)
# # step 10 part of speech tag the tokens with their POS tags (se sono verbi aggetivi ecc )
# tagged_tokens = nltk.pos_tag(tokens)
# print("Tagged tokens:", tagged_tokens)

# #step 11 stemming: Ridurre le parole alla loro forma base, come la conversione "saltando" a "salto."
# # create stemmer object
# stemmerita = SnowballStemmer("italian")
# stemmed_tokens = [stemmerita.stem(token) for token in tokens]
# print("Stemmed tokens:", stemmed_tokens)

# #step 12 lemmatization: ottimizzazione dello stemming, riporta le parole nella sua radice in modo correto ES camminiamo->camminare
# mywords = ['migliore', 'camminiamo', 'mangiassimo', 'promisi', 'derivante']
# langdata = simplemma.load_data('it')
# result = []
# for word in mywords:
#     result.append(simplemma.lemmatize(word, langdata))
# print(result)