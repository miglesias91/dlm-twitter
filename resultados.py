
import json

from pymongo import MongoClient

class Resultados:
    def __init__(self):
        with open('conexiones.json') as c:
            j = json.load(c)
            
        usuario = j['resultados']['usuario']
        pwd = j['resultados']['pwd']
        server = j['resultados']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).resultados

    def frecuencias(self, fecha=None, diario=None, categorias=None, terminos=True, verbos=True, personas=True, top=10):
        query = {}

        if fecha:
            if type(fecha) is list:
                query['fecha']={"$gte":fecha[0], "$lte": fecha[1]}
            else:
                query['fecha']=fecha

        if diario:
            query['diario']=diario

        if categorias:
            if type(categorias) is list:
                query['categoria']={"$in":categorias}
            else:
                query['categoria']=categorias

        freq_total = {}
        f_ter, f_ver, f_per = {}, {}, {}
        for f in self.bd.frecuencias.find(query):
            if terminos:
                f_ter = self.sumar_freqs(f['ter_tit'], f['ter_txt'], top)

            if verbos:
                f_ver = self.sumar_freqs(f['ver_tit'], f['ver_txt'], top)

            if personas:
                f_per = self.sumar_freqs(f['per_tit'], f['per_txt'], top)

            f_todo = self.sumar_freqs(f_ter, f_ver, top)
            f_todo = self.sumar_freqs(f_todo, f_per, top)

            freq_total = self.sumar_freqs(freq_total, f_todo, top)

        return freq_total

    def sumar_freqs(self, freqs, freqs_nuevas, top):
        for k, v in freqs_nuevas.items():
            if k in freqs:
                freqs[k] += v
            else:
                freqs[k] = v
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

