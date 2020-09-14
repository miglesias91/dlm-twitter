
import getopt, sys
import os
import json

import tweepy

from resultados import Resultados
from escritor import Escritor
from visualizador import Visualizador
from cm import CM

class Twittero:
    def __init__(self):
        pass

    def etiqueta():
        pass

    def resumen_semanal_dlm(self, fecha, diario, categorias):
        pass

    def postear_en_dlm(self, fecha, diario, categorias):
        resultados = Resultados()
        visu = Visualizador()
        tolkien = Escritor()

        if '-' in categorias:
            categorias = categorias.split('-')
        else:
            categorias = [categorias]

        freqs = resultados.frecuencias(fecha=fecha, diario=diario, categorias=categorias, top=20,verbos=False)
        if not bool(freqs):
            return

        path_imagen = os.getcwd() + '/imagenes/' + diario + '-todo.png'
        visu.nube(path_imagen, freqs, con_espacios=False)
        texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario)

        textos_e_imagenes = [{'media': [path_imagen], 'texto': texto}]

        for c in categorias:
            freqs = resultados.frecuencias(fecha=fecha, diario=diario, categorias=c, top=20, verbos=False)
            if not bool(freqs):
                continue

            path_imagen = os.getcwd() + '/imagenes/' + diario + '-' + c + '.png'
            visu.nube(path_imagen, freqs, con_espacios=False)
            texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario, categorias=c)

            textos_e_imagenes.append({'media': [path_imagen], 'texto': texto})

        cm = CM()
        cm.twittear_hilo('dicenlosmedios', textos_e_imagenes)

    def postear_en_discursosdeaf(self, fecha):
        fecha = parametros['fecha']

        kiosco = Kiosco()
        textos = [noticia['texto'] for noticia in kiosco.noticias(diario='casarosada', categorias='', fecha=fecha)]

        if len(textos) == 0:
            return

        nlp = NLP()
        nlp.separador = ''
        
        cm = CM()
        for texto in textos:

            # tw_intro = tweet_intro(texto, string_fecha) # ACA ESTA EL ERROR; STRING FECHA ESTA EN FORMADO MM.DD.YYYY, DEBERIA ESTAR EN YYYY.MM.DD
            tw_intro = tweet_intro(texto, fecha)

            kiosco = Kiosco()

            top_terminos = nlp.top_terminos(textos=[texto], n=15)
            top_verbos = nlp.top_verbos(textos=[texto], n=15)

            tw_terminos = tweet_terminos(top_terminos)
            tw_verbos = tweet_verbos(top_verbos)

            cm.twittear_hilo('discursosdeaf', )
            if parametros['twittear']:
                utiles.twittear_hilo([tw_intro, tw_terminos, tw_verbos], cuenta="dlp")
        
    def postear_en_discursosdemm(self, fecha):
        pass

def usage():
    print("twittero (twitter dicenlosmedios, discursosdeaf, discursosdemm) v1.0")
    print("./twittero.py dicenlosmedios [fecha] [diario] [categoria]")
    print("./twittero.py discursosdeaf [fecha]")
    print("./twittero.py discursosdemm [fecha]")

def main():
    accion = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage(None)
        sys.exit(2)
    
    for o, a in opts:
        if o == "--help" or o == "-h":
            print("twittero (twitter dicenlosmedios, discursosdeaf, discursosdemm) v1.0")
            print("./twittero.py dicenlosmedios [fecha] [diario] [categoria]")
            print("./twittero.py discursosdeaf [fecha]")
            print("./twittero.py discursosdemm [fecha]")
            return
        else:
            assert False, "opción desconocida"

    cuenta = args[0] 
    fecha = args[1]
    diario = args[2]
    categorias = args[3]

    t = Twittero()
    if cuenta == 'dicenlosmedios':
        t.postear_en_dlm(fecha=fecha, diario=diario, categorias=categorias)
    elif cuenta == 'discursosdeaf':
        pass
    elif cuenta == 'discursosdemm':
        pass

if __name__ == "__main__":
    main()        