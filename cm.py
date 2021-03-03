
import json
import tweepy

class CM:
    def __init__(self):
        pass

    def twittear_texto(self, cuenta, texto):
        api = self.api(cuenta)
        api.update_status(status=texto)


    def twittear_hilo(self, cuenta, textos_e_imagenes):
        api = self.api(cuenta)

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