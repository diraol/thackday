# encoding=utf-8

import sgmllib

class TableParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.tables = []
        self.inside_mytable = 0
	self.i = 0

    def start_table(self, attributes):
        "Process a table"

        for attr, val in attributes:
		if attr == "class" and val == "contacts":
			self.inside_mytable = 1

    def end_table(self):
        "Record the end of a table element."

        self.inside_mytable = 0

    def handle_data(self, data):
        "Handle the textual 'data'."

        if self.inside_mytable:
		self.tables.append(data)
    def get_tables(self):
        "Return a list of tables."

        return self.tables

import urllib, sgmllib
import time
import datetime

# Get something to work with.

#now = datetime.datetime.now()
#ano = now.year
#mes = now.month

ano = "2009"
mes = "1"

from lista_vereadores import lista_vereadores

for vereador in lista_vereadores:
    print "VEREADOR:", vereador["nome"]

    url = "http://www3.camara.sp.gov.br/saegPesq.asp?AnoPesq=%s&mesPesq=%s&vereador=%s" % (ano, mes, vereador["id"])
    f = urllib.urlopen(url)
    table_parser = TableParser()
    table_parser.parse(f.read())
    dados = table_parser.get_tables()

    result = "{| border=1\n"
    indice = 0
    for dado in dados:
	    if indice%2:
		    result += "|| %s\n" % dado
	    else:
		    result += "|--\n| %s " % dado
	    indice += 1

    result += "|}\n"
    result = result.decode("latin1")
    
    url = "http://vereadores.wikia.com/index.php?title=Especial:Exportar&pages=%s&action=submit" % vereador["artigo"]
    f = urllib.urlopen(url)
    artigo = f.read().decode("utf-8")

    artigo = artigo.split('<text xml:space="preserve">')[1]
    artigo = artigo.split("</text>")[0]

    partes_artigo = artigo.split("[[Categoria:")
    partes_artigo[0] = partes_artigo[0] + "\n\n<!-- BOT:TransparênciaVereadores:INICIO -->\n<!-- Tabela gerada dinamicamente a partir do site http://www3.camara.sp.gov.br/. Não edite. A tabela é automaticamente atualizada de tempos em tempos. -->\n\n== Tabela ==\n".decode("utf-8") +result + "\n<!-- BOT:TransparênciaVereadores:FIM -->\n\n".decode("utf-8")
    novo_artigo = "[[Categoria:".join(partes_artigo)
    
    print "novo artigo:" , novo_artigo
    print "TODO: salva_artigo_wiki(\"" + vereador["artigo"] + "\", novo_artigo)\n\n"

