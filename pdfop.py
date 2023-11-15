from PyPDF2 import PdfReader
from preprocessing import PreprocessingTesto
from preprocessing import Preprocessing
import fitz 
import re


class PdfOp:
    def __init__(self,path):
          self.my_dict = dict()
          self.mypath = path
          with open(path, 'rb') as pdf_file:
            self.reader = PdfReader(path)

    def get_dict(self):
       return self.my_dict

    def lettura_pagina(self,numero_pag):

        if numero_pag < 0  or numero_pag > len(self.reader.pages):
          print("Numero di pagina non valido.")
          return None
        
        pagina = self.reader.pages[numero_pag].extract_text()
        return pagina
    
    def lettura_completa(self):
      full_text = []
      pre_elaborazione=PreprocessingTesto()
      numero_pag = 22
      i = 1
      index = True
      fine_libro = False
      testo_rettangolo_capitolo = self.estrai_testo_da_rettangolo(numero_pag)
      pre_elaborazione.set_text(testo_rettangolo_capitolo)
      pre_elaborazione.clean_text()
      pre_elaborazione.lowercasing()
      pre_elaborazione.remove_url()
      pre_elaborazione.remove_punctuation()
      pre_elaborazione.remove_whitespace()
      testo_elaborato = pre_elaborazione.get_text()
      testo_elaborato = testo_elaborato.replace("\n", " ")
      pattern_capitolo = re.compile(r'\bcapitolo {}\b'.format(i))
      match_capitolo = re.findall(pattern_capitolo, testo_elaborato)
      page_text = self.reader.pages[numero_pag].extract_text()
      numero_pag +=1
      if len(page_text) != 0:
        preprocess = Preprocessing(page_text)
        testo_capitolo,cleaned_sentences_with_stopwords,tfidf_vectors = preprocess.doall()
        full_text.append(testo_capitolo)
        if match_capitolo:
          nome_capitolo = testo_elaborato
          self.my_dict[nome_capitolo] = []
          i+=1
        while numero_pag < 899:
          testo_rettangolo_capitolo = self.estrai_testo_da_rettangolo(numero_pag)
          pre_elaborazione.set_text(testo_rettangolo_capitolo)
          pre_elaborazione.clean_text()
          pre_elaborazione.lowercasing()
          pre_elaborazione.remove_url()
          pre_elaborazione.remove_punctuation()
          pre_elaborazione.remove_whitespace()
          testo_elaborato = pre_elaborazione.get_text()
          testo_elaborato = testo_elaborato.replace("\n", " ")
          pattern_capitolo = re.compile(r'\bcapitolo {}\b'.format(i))
          match_capitolo = re.findall(pattern_capitolo, testo_elaborato)
          page_text = self.reader.pages[numero_pag].extract_text()
          if len(page_text) !=0 and not match_capitolo:
            preprocess = Preprocessing(page_text)
            testo_capitolo,cleaned_sentences_with_stopwords,tfidf_vectors = preprocess.doall()
            full_text.append(testo_capitolo)
            numero_pag += 1
            if numero_pag-1== 897:
              list(self.my_dict.values())[i-2].append(full_text)
          else :
            numero_pag += 1
            if match_capitolo:
              nome_capitolo = testo_elaborato
              chiave = list(self.my_dict.keys())[i-2]
              match_key = re.findall(pattern_capitolo, chiave)
              if not match_key:
                  self.my_dict[nome_capitolo] = []
                  list(self.my_dict.values())[i-2].append(full_text)
                  list(self.my_dict.keys())[i-1] = nome_capitolo
                  full_text = []
                  preprocess = Preprocessing(page_text)
                  testo_capitolo,cleaned_sentences_with_stopwords,tfidf_vectors = preprocess.doall()
                  full_text.append(testo_capitolo)
                  i+=1
          
               
        
        return self.my_dict
      
    def divisione_capitolo(self):
      testo = self.lettura_completa() 
      pre_elaborazione_testo = PreprocessingTesto(testo)
      pre_elaborazione_testo.lowercasing()
      pre_elaborazione_testo.remove_url()
      pre_elaborazione_testo.remove_whitespace()
      pre_elaborazione_testo.remove_punctuation()

      return pre_elaborazione_testo.get_text()
    
    def estrazione_no_header(self,pag_num):
    # Apri il documento PDF
      altezza_header = 50
      pdf_documento = fitz.open(self.mypath)

      pagina = pdf_documento[pag_num]
      # Ottieni le dimensioni della pagina
      dimensioni_pagina = pagina.rect
      
      # print(dimensioni_pagina[1])
      # print(pagina.rect.y0)
      # Calcola le nuove coordinate per ritagliare escludendo l'altezza dell'header
      #rettangolo (x0, y0, x1 y1)
      nuove_coordinate = (dimensioni_pagina[0], dimensioni_pagina[1]+80,
                          dimensioni_pagina[2], dimensioni_pagina[3])
      

      # Estrai la porzione della pagina escludendo l'header
      porzione_pagina = pagina.get_text("text", clip=nuove_coordinate)
      pdf_documento.close()

      return porzione_pagina

    def estrai_testo_da_rettangolo(self,pagina_numero):

      #Specifica le coordinate del rettangolo (x0, y0, x1, y1)
      coordinate=(30, 30, 600, 300)
      pdf_documento = fitz.open(self.mypath)

      # Seleziona la pagina desiderata
      pagina = pdf_documento[pagina_numero]

      # Estrai il testo all'interno del rettangolo utilizzando le coordinate fornite
      testo_estratto = pagina.get_text("text", clip=coordinate)

      # Chiudi il documento PDF
      pdf_documento.close()

      return testo_estratto



       
      
    
