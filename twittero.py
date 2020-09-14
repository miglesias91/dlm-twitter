
import getopt, sys
import os
import json
import datetime

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
        resultados = Resultados()
        kiosco = Kiosco()
        visu = Visualizador()
        tolkien = Escritor()

        # recupero frecuencias del discurso
        freqs_por_hora = resultados.frecuencias_sin_agrupar(fecha=fecha, diario='casarosada', top=20,verbos=False)
        if not bool(freqs_por_hora):
            return
        
        cm = CM()
        for freq_y_hora in freqs_por_hora:
            hora = freq_y_hora['categoria']
            fecha_discurso = datetime.datetime.strptime(fecha+hora, '%Y%m%d%H%M%S')

            # recupero texto del discurso
            discurso = kiosco.noticias(fecha=fecha_discurso, diario='casarosada')[0]
            
            # armo tweet con el discurso en imagenes
            paths_imagenes = visu.texto_en_imagenes(discurso['texto'], 'calibri.ttf', 17, 800, 600, os.getcwd() + "/imagenes/intro")
            tw_intro = {
                'texto': "Análisis de discurso del " + tolkien.separar_fecha(fecha=fecha) + " de #AlbertoFernández.",
                'media': paths_imagenes
                }

            # armo textos del tweet
            txt_terminos = tolkien.texto_tweet_terminos_discurso(freq_y_hora['ter_txt'])
            txt_verbos = tolkien.texto_tweet_verbos_discurso(freq_y_hora['ver_txt'])

            # armo tweet con top 15 de terminos
            path_imagen_terminos = os.getcwd() + '/imagenes/terminos_discurso.png'
            etiquetas_terminos = [nombre for nombre, m in freq_y_hora['ter_txt'].items()][:15]
            data_terminos = [m for nombre, m in freq_y_hora['ter_txt'].items()][:15]
            visu.lollipop(path=path_imagen_terminos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de términos", etiquetas=etiquetas_terminos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_terminos)
            tw_terminos = {
                'texto': txt_terminos,
                'media': [path_imagen_terminos]
                }

            # armo tweet con top 15 de verbos
            path_imagen_verbos = os.getcwd() + '/imagenes/verbos_discurso.png'
            etiquetas_verbos = [nombre for nombre, m in freq_y_hora['ver_txt'].items()][:15]
            data_verbos = [m for nombre, m in freq_y_hora['ver_txt'].items()][:15]
            visu.lollipop(path=path_imagen_verbos, colormap=visu.cmap_del_dia(), titulo="Frecuencia de verbos", etiquetas=etiquetas_verbos, unidad="cantidad de apariciones", valfmt="{x:.0f}", data=data_verbos)
            tw_verbos = {
                'texto': txt_verbos,
                'media': [path_imagen_verbos]
                }

            # el CM twittea
            cm.twittear_hilo('discursosdeaf', [tw_intro, tw_terminos, tw_verbos])
        
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

    t = Twittero()
    if cuenta == 'dicenlosmedios':
        diario = args[2]
        categorias = args[3]

        t.postear_en_dlm(fecha=fecha, diario=diario, categorias=categorias)
    elif cuenta == 'discursosdeaf':
        t.postear_en_discursosdeaf(fecha=fecha)
    elif cuenta == 'discursosdemm':
        pass

if __name__ == "__main__":
    main()        