from preprocessing import Preprocessing
from preprocessing import AnswerMe
from preprocessing import PreprocessingTesto
from pdfop import PdfOp
from PyPDF2 import PdfReader
from autocorrect import Speller
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import pickle
import re


#LETTURA DI UN PDF ED ESTRAZIONE DEL TESTO
risposta = AnswerMe()
elaboratore_pdf = PdfOp("ManualePraticoJava.pdf")
numero_pagina = 35
testo_pagina = elaboratore_pdf.lettura_pagina(numero_pagina)
my_dict = dict()

#Serializziamo il dizionario in binario e lo salviamo in un file
#cosi da risparmiare tempo e non richiamare la funzione costosa
try:
    with open('my_dict.pickle', 'rb') as file:
        my_dict = pickle.load(file)
except FileNotFoundError:
    my_dict = elaboratore_pdf.lettura_completa()
    with open('my_dict.pickle', 'wb') as file:
        pickle.dump(my_dict , file)



# percorso_file = "output.txt"

# # Apri il file in modalità scrittura
# with open(percorso_file, 'w') as file:
#     # Itera attraverso gli elementi della lista e scrivili su file
#     for elemento in list(my_dict.values())[8]:
#         file.write(str(elemento) + '\n')

#TEST2 PRE-ELABORAZIONE TESTO PAGINA PDF 
# pre_elaborazione_pdf = PreprocessingTesto(testoprova)
# pre_elaborazione_pdf.clean_text()
# pre_elaborazione_pdf.remove_url()
# pre_elaborazione_pdf.remove_whitespace()
# pre_elaborazione_pdf.remove_punctuation()
# pre_elaborazione_pdf.lowercasing()

# pattern_capitolo = re.compile(r'\bcapitolo \d+\b')
# match_capitolo = re.findall(pattern_capitolo, pre_elaborazione_pdf.get_text())
# #print(match_capitolo)



preprocess = Preprocessing(testo_pagina)
cleaned_sentences,cleaned_sentences_with_stopwords,tfidf_vectors = preprocess.doall()
#print(cleaned_sentences)
user_question = "cos'è il timesharing?"

#define method
method = 1
question = preprocess.clean_sentence(user_question, stopwords=True)
question_embedding = preprocess.TFIDF_Q(question)
similarity_heap = AnswerMe.RetrieveAnswer(question_embedding , tfidf_vectors ,method)
print("\nQuestion: ", user_question)

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