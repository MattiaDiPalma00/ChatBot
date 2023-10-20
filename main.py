from preprocessing import Preprocessing
from pdfop import PdfOp
from PyPDF2 import PdfReader
from autocorrect import Speller
from nltk.stem.snowball import SnowballStemmer


# #nltk.download()
text = "CIAOou ssono mattia, e QUESTOu è un testoot vai a www.esempio.it o https://www.freecodecamp.org/learn/back-end-development-and-apis/mongodb-and-mongoose/install-and-set-up-mongoose"

elaboratore = Preprocessing(text)
#step 1 tokenizzazione: dividere il testo in parole individuali(token)
elaboratore.tokenizzazione()

#step 2 lowercasing : rendere le maiuscole minuscole 
elaboratore.lowercasing()
print("lower tokens :",elaboratore.lower_case_token)

#step 3 remove punctuation
elaboratore.remove_punctuation()
print ("tokens senza punteggiatura:",elaboratore.filtered_token)

#step 4 remove punctuationstopwords in italian (es il e ecc..)
elaboratore.remove_stopword()
print("Tokens without stopwords:", elaboratore.nostopwords_tokens)

#step 5 remove whitespace: replace multiple consecutive white space characters with a single space
elaboratore.remove_whitespace()
print("Cleaned text:", elaboratore.text_nospace)

# step 6 remove url 
elaboratore.remove_url()
print("Testo pulito senza URL:", elaboratore.text_nourl)

# #step 7 remove parole frequenti 
# fdist = nltk.FreqDist(tokens)
# # remove the most common words (e.g., the top 10% of words by frequency)
# filtered_tokens = [token for token in tokens if fdist[token] < fdist.N() * 0.1]
# print("Text senza parole frequenti :", filtered_tokens)

#step 9 spelling correction
elaboratore.spelling_correction()
print("Testo originale:", text)
print("Testo corretto:", elaboratore.testo_corretto)

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

#TEST LETTURA DI UN PDF ED ESTRAZIONE DEL TESTO
#reader = PdfReader("Tracciaprogetto.pdf")
elaboratore_pdf = PdfOp("ManualePraticoJava.pdf")
numero_pagina = 22
testo_pagina = elaboratore_pdf.lettura_pagina(numero_pagina)
print (f"pagina {numero_pagina}:\n{testo_pagina}")

# def leggi_pagina_pdf(file_path, numero_pagina):
#     # Apre il file PDF in modalità lettura binaria ('rb')
#     with open(file_path, 'rb') as pdf_file:
#         pdf_reader = PdfReader(pdf_file)

#         # Verifica che il numero di pagina sia valido
#         if numero_pagina < 0 :
#             print("Numero di pagina non valido.")
#             return None

#         # Estrae la pagina specificata
#         pagina = pdf_reader.pages[(numero_pagina)]

#         # Estrae il testo dalla pagina
#         testo_pagina_nuovo = pagina.extract_text()
        
#         return testo_pagina_nuovo
    

# # Esempio di utilizzo
# file_path = 'ManualePraticoJava.pdf'
# paginatest = reader.pages[21].extract_text()

# numero_pagina = 20  # Cambia con il numero di pagina che desideri leggere
# testo_pagina = leggi_pagina_pdf(file_path, numero_pagina)

#if testo_pagina:
   # print(f"Testo della pagina {numero_pagina}:\n{testo_pagina}")

# #Estrazione testo dalla pagina 1 
# paragrafo = page.extract_text()
# pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"

# cleaned_paragrafo = re.sub(pattern, "", paragrafo)


# tokenspdf = nltk.word_tokenize(cleaned_paragrafo)
# lower_case_token = [token.lower() for token in tokenspdf]
# filtered_token = [token for token in lower_case_token if token not in string.punctuation]

# print ("tokens senza punteggiatura:",filtered_token)

