
import json

from pymongo import MongoClient

class Resultados:
    def __init__(self):
        with open('conexiones-oracle.json') as c:
            j = json.load(c)
            
        usuario = j['resultados']['usuario']
        pwd = j['resultados']['pwd']
        server = j['resultados']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).resultados

    def frecuencias(self, fecha=None, diario=None, secciones=None, sustantivos=True, verbos=True, entidades=True, adjetivos=True, top=10):
        query = {}

        if fecha:
            if type(fecha) is list:
                query['fecha']={"$gte":fecha[0], "$lte": fecha[1]}
            else:
                query['fecha']=fecha

        if diario:
            query['diario']=diario

        if secciones:
            if type(secciones) is list:
                query['seccion']={"$in":secciones}
            else:
                query['seccion']=secciones

        freq_total = {}
        fsus, fver, fent = {}, {}, {}
        for f in self.bd.frecuencias.find(query):
            if sustantivos:
                fsus = self.sumar_freqs(f['sustit'], f['sustxt'], top)

            if adjetivos:
                fadj = self.sumar_freqs(f['adjtit'], f['adjtxt'], top)

            if verbos:
                fver = self.sumar_freqs(f['vertit'], f['vertxt'], top)

            if entidades:
                fent = self.sumar_freqs(f['enttit'], f['enttxt'], top)

            f_todo = self.sumar_freqs(fsus, fadj, top)
            f_todo = self.sumar_freqs(f_todo, fver, top)
            f_todo = self.sumar_freqs(f_todo, fent, top)

            freq_total = self.sumar_freqs(freq_total, f_todo, top)

        return freq_total

    def frecuencias_sin_agrupar(self, fecha=None, diario=None, secciones=None, top=10):
        query = {}

        if fecha:
            if type(fecha) is list:
                query['fecha']={"$gte":fecha[0], "$lte": fecha[1]}
            else:
                query['fecha']=fecha

        if diario:
            if type(diario) is list:
                query['diario']={"$in":diario}
            else:
                query['diario']=diario

        if secciones:
            if type(secciones) is list:
                query['seccion']={"$in":secciones}
            else:
                query['seccion']=secciones

        return [n for n in self.bd.frecuencias.find(query)]

    def sumar_freqs(self, freqs, freqs_nuevas, top):
        for k, v in freqs_nuevas.items():
            if k in freqs:
                freqs[k] += v
            else:
                freqs[k] = v
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

