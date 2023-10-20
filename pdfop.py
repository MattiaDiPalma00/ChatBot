from PyPDF2 import PdfReader

class PdfOp:
    def __init__(self,path):
          with open(path, 'rb') as pdf_file:
           self.reader = PdfReader(path)
    
    def lettura_pagina(self,numero_pag):

        if numero_pag < 0  or numero_pag > len(self.reader.pages):
          print("Numero di pagina non valido.")
          return None
        
        pagina = self.reader.pages[numero_pag].extract_text()
        return pagina