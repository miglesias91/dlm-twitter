import datetime
import dateutil
import json

import pymongo
from pymongo import MongoClient

class Kiosco:
    def __init__(self, fecha=None):
        with open('conexiones.json') as c:
            j = json.load(c)
            
        usuario = j['kiosco']['usuario']
        pwd = j['kiosco']['pwd']
        server = j['kiosco']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).dlm

    def noticias(self, fecha=None, diario=None, categorias=None, fecha_in=True, url_in=True, diario_in=True, cat_in=True, tit_in=True, text_in=True):
        query = {}

        if fecha:
            if type(fecha) is dict:
                desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
                hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
            else:
                desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
                hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
            query['fecha']={"$gte":desde, "$lte":hasta}

        if diario:
            query['diario']=diario

        if categorias:
            if len(categorias) > 0:
                query['cat']={"$in":categorias}

        cursor = self.bd.noticias.find(query)

        return [n for n in cursor]

