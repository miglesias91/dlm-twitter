
import getopt, sys
import json

import tweepy

from resultados import Resultados

class Twittero:
    def __init__(self):
        pass

    def postear_en_dlm(self, fecha, diario, categoria):
        resultados = Resultados()

        freqs = resultados.frecuencias(fecha=fecha, diario=diario, categorias=categoria, verbos=False)

        texto = "Tendencias en las noticias de #" + categoria + " de #" + diario + " del " + fecha + "\n"
        i = 0
        for nombre, m in freqs.items():
            linea = ""
            i += 1
            if i >= 10:
                linea = str(i) + ". #" + nombre.replace(' ','') + " " + str(m) + "\n"
                texto += linea
                break
            else:
                linea = str(i) + ".  #" + nombre.replace(' ','') + " " + str(m) + "\n"

            if len(texto) + len(linea) > 220:
                break
            else:
                texto += linea

        api = self.api('dicenlosmedios')

        api.update_status(status=texto)

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
    categoria = args[3]

    t = Twittero()
    if cuenta == 'dicenlosmedios':
        t.postear_en_dlm(fecha=fecha, diario=diario, categoria=categoria)
    elif cuenta == 'discursosdeaf':
        pass
    elif cuenta == 'discursosdemm':
        pass

if __name__ == "__main__":
    main()        