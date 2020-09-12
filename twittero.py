
import getopt, sys
import os
import json

import tweepy

from resultados import Resultados
from escritor import Escritor
from visualizador import Visualizador

class Twittero:
    def __init__(self):
        pass

    def etiqueta():
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
        path_imagen = os.getcwd() + '/imagenes/' + diario + '-todo.png'
        visu.nube(path_imagen, freqs, con_espacios=False)
        texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario)

        textos_e_imagenes = [{'media': [path_imagen], 'texto': texto}]

        for c in categorias:
            freqs = resultados.frecuencias(fecha=fecha, diario=diario, categorias=c, top=20, verbos=False)
            path_imagen = os.getcwd() + '/imagenes/' + diario + '-' + c + '.png'
            visu.nube(path_imagen, freqs, con_espacios=False)
            texto = tolkien.tweet_tendencias(freqs=freqs, fecha=fecha, diario=diario, categorias=c)

            textos_e_imagenes.append({'media': [path_imagen], 'texto': texto})

        api = self.api('dicenlosmedios')

        id_a_responder = 0
        for texto_e_imagen in textos_e_imagenes:
            medias = []
            for path_img in texto_e_imagen['media']:
                media = api.media_upload(path_img)
                medias.append(media)
                if len(medias) >= 4:
                    break
            estado = api.update_status(status=texto_e_imagen['texto'], in_reply_to_status_id=id_a_responder, auto_populate_reply_metadata=True, media_ids=[media.media_id for media in medias])
            id_a_responder = estado.id

    def postear_en_discursosdeaf(self, fecha):
        pass
        
    def postear_en_discursosdemm(self, fecha):
        pass

    def api(self, cuenta):
        claves = open("twitter.keys", "r")
        json_claves = json.load(claves)
        
        consumer_key = json_claves[cuenta]['consumer_key']
        consumer_secret = json_claves[cuenta]['consumer_secret']
        access_token = json_claves[cuenta]['access_token']
        access_token_secret = json_claves[cuenta]['access_token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return tweepy.API(auth)

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