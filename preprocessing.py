import nltk
import string
import re
import numpy as np
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from autocorrect import Speller
import heapq
from sklearn.feature_extraction.text import TfidfVectorizer 

class Preprocessing:
    #constructor
    def __init__(self,txt):
        # Tokenization
        tokens = nltk.sent_tokenize(txt) 
        self.tokens = tokens
        self.text = txt
        self.tfidfvectoriser=TfidfVectorizer()

    # Data Cleaning
    # remove extra spaces
    # convert sentences to lower case 
    # remove stopword
    def clean_sentence(self, sentence, stopwords=False):
        sentence = sentence.lower().strip()
        pattern = r'\b[\w-]+\b'  #pattern per parola con in mezzo simboli particolari
        pattern_url = r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
        sentence= re.sub(pattern_url,' ', sentence) #elimina url
        sentence = re.sub(r'(-)', '', sentence)
        sentence = re.sub(r'(—)', '', sentence)
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


class AnswerMe:
    #cosine similarity
    def Cosine(self, question_vector, sentence_vector):
        dot_product = np.dot(question_vector, sentence_vector.T)
        denominator = (np.linalg.norm(question_vector) * np.linalg.norm(sentence_vector))
        return dot_product/denominator
    
    #Euclidean distance
    def Euclidean(self, question_vector, sentence_vector):
        vec1 = question_vector.copy()
        vec2 = sentence_vector.copy()
        if len(vec1)<len(vec2): vec1,vec2 = vec2,vec1
        vec2 = np.resize(vec2,(vec1.shape[0],vec1.shape[1]))
        return np.linalg.norm(vec1-vec2)

    # main call function
    def answer(self, question_vector, sentence_vector, method):
        if method==1: return self.Euclidean(question_vector,sentence_vector)
        else: return self.Cosine(question_vector,sentence_vector)
    
    def RetrieveAnswer(question_embedding, tfidf_vectors,method=1):
        similarity_heap = []
        if method==1: max_similarity = float('inf')
        else: max_similarity = -1
        index_similarity = -1

        for index, embedding in enumerate(tfidf_vectors):  
            find_similarity = AnswerMe()
            similarity = find_similarity.answer((question_embedding).toarray(),(embedding).toarray() , method).mean()
            if method==1:
                heapq.heappush(similarity_heap,(similarity,index))
            else:
                heapq.heappush(similarity_heap,(-similarity,index))
                
        return similarity_heap


class PreprocessingTesto:
    def __init__(self,testo = ""):
        if testo is not None:
            self.testo = testo 
        else:
            self.testo = "" 

    
    def set_text(self,testo):
        self.testo = testo
    
    def get_text(self):
        return self.testo
    
    #step 1 tokenizzazione: dividere il testo in parole individuali(token)
    def clean_text(self):
        pattern = r'\b[\w-]+\b'  #pattern per parola con in mezzo simboli particolari 
        self.testo = re.sub(r'(-) ', r'\1', self.testo)  # Rimuovi gli spazi dopo i trattini

        # words = re.findall(pattern,self.testo)

        # words = [re.sub('-', '', word) for word in words]
        # self.tokens = nltk.sent_tokenize(' '.join(words))

    #step 2 lowercasing : rendere le maiuscole minuscole 
    def lowercasing(self):
        #self.tokens = [token.lower() for token in self.tokens]
        self.testo = self.testo.lower()

    #step 3 remove punctuation
    def remove_punctuation(self):
        #self.tokens = [token for token in self.tokens if token not in string.punctuation]
        punctuations = set(string.punctuation)
        # Rimuovi i caratteri di punteggiatura dalla stringa
        self.testo= ''.join(char for char in self.testo if char not in punctuations)
    
    #step 4 remove punctuationstopwords in italian (es il e ecc..)
    def remove_stopword(self):
        stopwords = nltk.corpus.stopwords.words("italian")
        #self.tokens = [token for token in self.tokens if token.lower() not in stopwords]

    #step 5 remove whitespace: replace multiple consecutive white space characters with a single space
    def remove_whitespace(self):
        self.testo = self.testo.strip()
        #self.testo = ' '.join(self.testo.split())
    
    #step 6 remove url 
    def remove_url(self):
        pattern = r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
        self.testo = re.sub(pattern,' ', self.testo)
      

    #step 7 spelling correction
    # def spelling_correction(self):
    #     # Crea un oggetto Speller per la lingua italiana
    #     spell = Speller(lang='it')
    #     correzioni = [spell(token) for token in self.tokens]
    #     #self.tokens = correzioni
    #     # Unisci le parole corrette in un testo corretto
    #     self.testo = ' '.join(correzioni)
    