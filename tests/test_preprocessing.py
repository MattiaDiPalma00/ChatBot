from preprocessing import Preprocessing
import string
import nltk
import re 

def test_tokenizzazione():
    # Crea un oggetto Preprocessing con un testo di esempio
    testo = "Test tokenizzazione su vari scenari " " con spazi e trat- tini ?  "
    pre_elaborazione = Preprocessing(testo)

    # Esegui la tokenizzazione
    pre_elaborazione.tokenizzazione()

    # Verifica che i risultati siano corretti
    assert pre_elaborazione.get_tokens() == ['Test', 'tokenizzazione', 'su', 'vari', 'scenari', 'con', 'spazi', 'e', 'trattini']

def test_lower_casing():
    
    testo = "TESTO Di pROvAa mAIuSCOLeEeE PEr tEst"
    pre_elaborazione = Preprocessing(testo)
    pre_elaborazione.tokenizzazione()
    pre_elaborazione.lowercasing()

    assert pre_elaborazione.get_tokens() == ['testo', 'di', 'provaa', 'maiuscoleeee', 'per', 'test']

def test_remove_punctuation():

    testo = "testo, prova???. ,, eliminazione... punteggiatura ,!. salve ciao..!!!"
    pre_elaborazione = Preprocessing(testo)
    pre_elaborazione.tokenizzazione()
    pre_elaborazione.remove_punctuation()

    for token in pre_elaborazione.get_tokens():
        assert token not in string.punctuation

def test_remove_stopword():
    stopwords = nltk.corpus.stopwords.words("italian")
    testo = "testo eliminare al ad allo ai le parole stopword e le ad "
    pre_elaborazione = Preprocessing(testo)
    pre_elaborazione.tokenizzazione()
    pre_elaborazione.remove_stopword()
    for token in pre_elaborazione.get_tokens():
        assert token not in stopwords

def test_remove_url():
    testo =  """https://www.w3schools.com/python/ref_keyword_assert.asp prova https://www.reverso.net/traduzione-testo#sl=eng&tl=ita&text=The%2520username%2520must%2520contain%2520only%2520letters%252C%2520numbers%252C%2520hyphens%2520and%2520underscores.
    test w url  https://www.youtube.com/watch?v=kTpR98afSpQ&t=100s"""

    pattern2 = re.compile(r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/\S*)?\b')
    pre_elaborazione_test = Preprocessing(testo)
    pre_elaborazione_test.remove_url()

    assert not pattern2.search(pre_elaborazione_test.get_text())
       
def test_remove_whitespace():
    testo = "testo per    eliminare   spazi in  più   prova test    "
    pre_elaborazione_test = Preprocessing(testo)
    pre_elaborazione_test.remove_whitespace()

    pattern = re.compile(r'\s{2,}')
    assert not pattern.search(pre_elaborazione_test.get_text())
    
    

    
    

    
