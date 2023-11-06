import nltk
import string
import re
import numpy as np
from autocorrect import Speller
import heapq
from sklearn.feature_extraction.text import TfidfVectorizer 

class Preprocessing:
    def __init__(self,testo):
        self.testo = testo 
        self.tfidfvectoriser=TfidfVectorizer()

    def get_tokens(self):
        return self.tokens
    
    def get_text(self):
        cleaned_sentences = []
        self.tokenizzazione()
        for line in self.tokens:
            cleaned = self.lowercasing()
            cleaned = self.remove_stopword()
            cleaned_sentences.append(cleaned)
        return cleaned_sentences
    
    #step 1 tokenizzazione: dividere il testo in parole individuali(token)
    def tokenizzazione(self):
        pattern = r'\b[\w-]+\b'  #pattern per parola con in mezzo simboli particolari 
        self.testo = re.sub(r'(-) ', r'\1', self.testo)  # Rimuovi gli spazi dopo i trattini

        words = re.findall(pattern,self.testo)

        words = [re.sub('-', '', word) for word in words]
        self.tokens = nltk.word_tokenize(' '.join(words))

    #step 2 lowercasing : rendere le maiuscole minuscole 
    def lowercasing(self):
        self.tokens = [token.lower() for token in self.tokens]
        self.testo.lower().split()

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
        self.testo = ' '.join(self.testo.split())
    
    #step 6 remove url 
    def remove_url(self):
        pattern = r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b'
        self.testo = re.sub(pattern,' ', self.testo)
      

    #step 7 spelling correction
    def spelling_correction(self):
        # Crea un oggetto Speller per la lingua italiana
        spell = Speller(lang='it')
        correzioni = [spell(token) for token in self.tokens]
        self.tokens = correzioni
        # Unisci le parole corrette in un testo corretto
        self.testo = ' '.join(correzioni)
    
    def TFIDF(self,testo):
        #fit addestra il modello sul testo per il calcolo dei vettori TF-idf
        self.tfidfvectoriser.fit(testo)
        tfidf_vectors=self.tfidfvectoriser.transform(testo)

        return tfidf_vectors
    
    def TFIDF_Q(self,question_to_be_cleaned):
        tfidf_vectors=self.tfidfvectoriser.transform([question_to_be_cleaned])
        return tfidf_vectors

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