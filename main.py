from preprocessing import Preprocessing
from pdfop import PdfOp
from PyPDF2 import PdfReader
from autocorrect import Speller
from nltk.stem.snowball import SnowballStemmer


# #nltk.download()
#text = "CIAOou ssono mattia, e QUESTOu è un testoot vai a www.esempio.it o https://www.freecodecamp.org/learn/back-end-development-and-apis/mongodb-and-mongoose/install-and-set-up-mongoose"

#TEST1 LETTURA DI UN PDF ED ESTRAZIONE DEL TESTO
#reader = PdfReader("Tracciaprogetto.pdf")
elaboratore_pdf = PdfOp("ManualePraticoJava.pdf")
numero_pagina = 20
testo_pagina = elaboratore_pdf.lettura_pagina(numero_pagina)
#if testo_pagina :cls
 #  print (f"pagina {numero_pagina}:\n{testo_pagina}")

#TEST2 PRE-ELABORAZIONE TESTO PAGINA PDF 
pre_elaborazione_pdf = Preprocessing(testo_pagina)
pre_elaborazione_pdf.remove_url()
pre_elaborazione_pdf.remove_whitespace()
pre_elaborazione_pdf.tokenizzazione()
pre_elaborazione_pdf.spelling_correction()
pre_elaborazione_pdf.lowercasing()
pre_elaborazione_pdf.remove_punctuation()
pre_elaborazione_pdf.remove_stopword()

print(f"token elaborati : {pre_elaborazione_pdf.get_tokens()}\n testo elaborato : {pre_elaborazione_pdf.get_text()}")


#elaboratore = Preprocessing(text)
# #step 1 tokenizzazione: dividere il testo in parole individuali(token)
# elaboratore.tokenizzazione()

# #step 2 lowercasing : rendere le maiuscole minuscole 
# elaboratore.lowercasing()
# print("lower tokens :",elaboratore.lower_case_token)

# #step 3 remove punctuation
# elaboratore.remove_punctuation()
# print ("tokens senza punteggiatura:",elaboratore.filtered_token)

# #step 4 remove punctuationstopwords in italian (es il e ecc..)
# elaboratore.remove_stopword()
# print("Tokens without stopwords:", elaboratore.nostopwords_tokens)

# #step 5 remove whitespace: replace multiple consecutive white space characters with a single space
# elaboratore.remove_whitespace()
# #print("Cleaned text:", elaboratore.text_nospace)

# # step 6 remove url 
# elaboratore.remove_url()
# # print("Testo pulito senza URL:", elaboratore.text_nourl)

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