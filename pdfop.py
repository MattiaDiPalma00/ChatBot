from PyPDF2 import PdfReader

class PdfOp:
    def __init__(self,path):
          self.reader = PdfReader(path)
    
    def lettura_pagina(self,numero_pag):
        pagina = self.reader.pages[numero_pag].extract_text()
        return pagina