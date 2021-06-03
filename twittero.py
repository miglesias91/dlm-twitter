
import getopt, sys
import os
import json
import datetime
import re

import tweepy

from bd.resultados import Resultados
from bd.kioscomongo import Kiosco
from escritor import Escritor
from visualizador import Visualizador
from cm import CM

class Twittero:
    def __init__(self):
        pass

    def etiqueta():
        pass

    def resumen_semanal_dlm(self, fecha, diario, secciones):
        pass

    def postear_en_dlm(self, fecha, diario, secciones):
        resultados = Resultados()
        visu = Visualizador()
        tolkien = Escritor()

        if '-' in secciones:
            secciones = secciones.split('-')
        else:
            secciones = [secciones]

        freqs = resultados.frecuencias(fecha=fecha, diario=diario, secciones=secciones, top=20,verbos=False)
        if not bool(freqs):
            return

        path_imagen = os.getcwd() + '/imagenes/' + diario + '-todo.png'
        visu.nube(path_imagen, freqs, con_espacios=False)
        texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario)

        textos_e_imagenes = [{'media': [path_imagen], 'texto': texto}]

        for s in secciones:
            freqs = resultados.frecuencias(fecha=fecha, diario=diario, secciones=s, top=20, verbos=False)
            if not bool(freqs):
                continue

            path_imagen = os.getcwd() + '/imagenes/' + diario + '-' + s + '.png'
            visu.nube(path_imagen, freqs, con_espacios=False)
            texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario, secciones=s)

            textos_e_imagenes.append({'media': [path_imagen], 'texto': texto})

        cm = CM()
        cm.twittear_hilo('dicenlosmedios', textos_e_imagenes)

    def postear_contador(self, fecha, concepto):
        resultados = Resultados()
        tolkien = Escritor()

        terminos = {
        'cfk' : ['CFK', 'Kirchner','Cristina', 'Cristina Kirchner', 'Cristina Fernández', 'Cristina Fernández de Kirchner', 'Cristina Fernández De Kirchner', 'Vicepresidenta'],
        'dolar' : ['dólar', 'US$', 'Dólar'],
        'corrupcion' : ['corrupción', 'corrupto', 'Corrupción'],
        'larreta' : ['Larreta', 'Horacio Larreta', 'Rodríguez Larreta', 'Horacio Rodríguez', 'Horacio Rodríguez Larreta'],
        'venezuela' : ['Venezuela', 'Nicolás Maduro', 'Maduro', 'Chávez', 'Hugo Chávez', 'Chavez', 'Hugo Chavez'],
        'inseguridad' : ['inseguridad', 'inseguro'],
        'miedo' : ['miedo', 'muerte', 'muerto', 'muerta','asesinato', 'horror']
        }

        tabla = {}
        for medio in [medio for medio in tolkien.hashtags.keys() if medio != 'casarosada']:

            freqs = resultados.frecuencias(fecha=fecha, diario=medio, verbos=False, top=2000)
            
            if not bool(freqs):
                continue
            
            total = sum([f[1] for f in freqs.items() if f[0] in terminos[concepto]])
            
            if total == 0:
                continue

            tabla[medio] = total

        if len(tabla) == 0:
            return
            
        ordenada = {k: v for k, v in sorted(tabla.items(), key=lambda item: item[1], reverse=True)}
        texto = tolkien.tweet_contador(concepto=concepto, freqs=ordenada, fecha=fecha)
        
        cm = CM()
        cm.twittear_texto('dicenlosmedios', texto) 

    def postear_en_discursosdeaf(self, fecha):
        resultados = Resultados()
        kiosco = Kiosco()
        visu = Visualizador()
        tolkien = Escritor()

        # recupero frecuencias del discurso
        freqs = resultados.bd.frecuencias_discursos.aggregate([{ '$match': { 'presidente': 'alberto' , 'fecha': fecha } }])

        if not bool(freqs):
            return
        
        cm = CM()
        for freq in freqs:

            # recupero texto del discurso
            discurso = kiosco.noticias(diario='casarosada', url=freq['url'])[0]
            
            # armo tweet con el discurso en imagenes
            texto = " ".join(re.split("\s+", discurso['texto'], flags=re.UNICODE))
            paths_imagenes = visu.texto_en_imagenes(texto, 'calibri.ttf', 17, 800, 600, os.getcwd() + "/imagenes/introaf")
            tw_intro = {
                'texto': "Discurso del " + tolkien.separar_fecha(fecha=freq['fecha']) + " de #AlbertoFernández. Hilo 👇",
                'media': paths_imagenes
                }

            # armo textos del tweet
            txt_sustantivos = tolkien.texto_tweet_sustantivos_discurso(freq['sustxt'])
            txt_adjetivos = tolkien.texto_tweet_adjetivos_discurso(freq['adjtxt'])

            # armo tweet con top 15 de terminos
            path_imagen_sustantivos = os.getcwd() + '/imagenes/sustantivos_discursoaf.png'
            etiquetas_sustantivos = [nombre for nombre, m in freq['sustxt'].items()][:15]
            data_sustantivos = [m for nombre, m in freq['sustxt'].items()][:15]
            visu.lollipop(path=path_imagen_sustantivos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de sustantivos", etiquetas=etiquetas_sustantivos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_sustantivos)
            tw_terminos = {
                'texto': txt_sustantivos,
                'media': [path_imagen_sustantivos]
                }

            # armo tweet con top 15 de verbos
            path_imagen_adjetivos = os.getcwd() + '/imagenes/adjetivos_discursoaf.png'
            etiquetas_adjetivos = [nombre for nombre, m in freq['adjtxt'].items()][:15]
            data_adjetivos = [m for nombre, m in freq['adjtxt'].items()][:15]
            visu.lollipop(path=path_imagen_adjetivos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de adjetivos", etiquetas=etiquetas_adjetivos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_adjetivos)
            tw_verbos = {
                'texto': txt_adjetivos,
                'media': [path_imagen_adjetivos]
                }

            # el CM twittea
            cm.twittear_hilo('discursosdeaf', [tw_intro, tw_terminos, tw_verbos])

    def postear_en_discursoshistoricos(self, cuenta, fecha=None):
        resultados = Resultados()
        kiosco = Kiosco()
        visu = Visualizador()
        tolkien = Escritor()

        presidente, subfijopng, hashtag = self.info_cuenta(cuenta)

        # recupero frecuencias al azar
        freqs = resultados.bd.frecuencias_discursos.aggregate([{ '$match': { 'presidente': presidente } }, { '$sample': { 'size': 1 } }])
        
        if not bool(freqs):
            return
        
        cm = CM()
        for freq in freqs:
            # recupero texto del discurso
            discurso = kiosco.noticias(diario='casarosada', url=freq['url'])[0]
            
            # armo tweet con el discurso en imagenes
            texto = " ".join(re.split("\s+", discurso['texto'], flags=re.UNICODE))
            paths_imagenes = visu.texto_en_imagenes(texto, 'calibri.ttf', 17, 800, 600, os.getcwd() + "/imagenes/intro" + subfijopng)
            # TODO: la fecha esta MAL. pasar de date a string.
            tw_intro = {
                'texto': "Discurso del " + tolkien.separar_fecha(fecha=freq['fecha']) + " de " + hashtag + ". Hilo 👇",
                'media': paths_imagenes
                }

            # armo textos del tweet
            txt_sustantivos = tolkien.texto_tweet_sustantivos_discurso(freq['sustxt'])
            txt_adjetivos = tolkien.texto_tweet_adjetivos_discurso(freq['adjtxt'])

            # armo tweet con top 15 de terminos
            path_imagen_sustantivos = os.getcwd() + '/imagenes/sustantivos_discurso' + subfijopng + '.png'
            etiquetas_sustantivos = [nombre for nombre, m in freq['sustxt'].items()][:15]
            data_sustantivos = [m for nombre, m in freq['sustxt'].items()][:15]
            visu.lollipop(path=path_imagen_sustantivos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de sustantivos", etiquetas=etiquetas_sustantivos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_sustantivos)
            tw_terminos = {
                'texto': txt_sustantivos,
                'media': [path_imagen_sustantivos]
                }

            # armo tweet con top 15 de verbos
            path_imagen_adjetivos = os.getcwd() + '/imagenes/adjetivos_discurso' + subfijopng + '.png'
            etiquetas_adjetivos = [nombre for nombre, m in freq['adjtxt'].items()][:15]
            data_adjetivos = [m for nombre, m in freq['adjtxt'].items()][:15]
            visu.lollipop(path=path_imagen_adjetivos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de adjetivos", etiquetas=etiquetas_adjetivos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_adjetivos)
            tw_verbos = {
                'texto': txt_adjetivos,
                'media': [path_imagen_adjetivos]
                }

            # el CM twittea
            cm.twittear_hilo(cuenta, [tw_intro, tw_terminos, tw_verbos])

    def info_cuenta(self, cuenta):
        if cuenta == 'discursosdeaf':
            return 'alberto', 'af', '#AlbertoFernández'
        elif cuenta == 'discursosdemm':
            return 'macri', 'mm', '#MauricioMacri'
        elif cuenta == 'discursosdecfk':
            return 'cristina', 'cfk', '#CFK'
        elif cuenta == 'discursosdenk':
            return 'nestor', 'nk', '#NéstorKirchner'

def usage():
    print("twittero (twitter dicenlosmedios, discursosdeaf, discursosdemm) v1.0")
    print("./twittero.py dicenlosmedios [fecha] [diario] [seccion]")
    print("./twittero.py discursosdeaf [fecha]")
    print("./twittero.py discursosdemm [(opcional) fecha]")
    print("./twittero.py discursosdecfk [(opcional) fecha]")
    print("./twittero.py discursosdenk [(opcional) fecha]")
    print("./twittero.py contador [concepto] [(opcional) fecha]")

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
            print("./twittero.py dicenlosmedios [fecha] [diario] [seccion]")
            print("./twittero.py discursosdeaf [fecha]")
            print("./twittero.py discursosdemm [(opcional) fecha]")
            print("./twittero.py discursosdecfk [(opcional) fecha]")
            print("./twittero.py discursosdenk [(opcional) fecha]")
            print("./twittero.py contador [concepto] [(opcional) fecha]")
            return
        else:
            assert False, "opción desconocida"

    cuenta = args[0]

    t = Twittero()
    if cuenta == 'dicenlosmedios':
        fecha = args[1]
        diario = args[2]
        secciones = args[3]

        t.postear_en_dlm(fecha=fecha, diario=diario, secciones=secciones)
    elif cuenta == 'contador':
        if len(args) == 1:
            print("Falta un argumento: ./twittero.py contador [concepto] [(opcional) fecha]")
        if len(args) == 2:
            fecha = datetime.date.today().strftime('%Y%m%d')
        else:
            fecha = args[2]

        concepto = args[1]
        t.postear_contador(fecha=fecha, concepto=concepto)
    elif cuenta == 'discursosdeaf':
        fecha = args[1]
        t.postear_en_discursosdeaf(fecha=fecha)
    else:
        t.postear_en_discursoshistoricos(cuenta)

if __name__ == "__main__":
    main()        