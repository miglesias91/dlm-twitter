import datetime

class Escritor:
    def __init__(self):
        self.hashtags = {
            'ambito': '#Ambito',
            'casarosada': '#CasaRosada',
            'clarin': '#Clarin',
            'eldestape': '#ElDestape',
            'infobae': '#Infobae',
            'lanacion': '#LaNacion',
            'paginadoce': '#Pagina12',
            'perfil': '#Perfil',
            'telam': '#Telam',
            'todonoticias': '#TN',
            'diariodeleuco': "#LeDoyMiPalabra",
            'cfk' : '#CFK',
            'dolar' : '#dólar',
            'corrupcion' : '#corrupción',
            'larreta' : '#Larreta',
            'venezuela' : '#Venezuela',
            'inseguridad' : '#inseguridad',
            'miedo' : '#miedo'
        }

    def tweet_contador(self, freqs, fecha, concepto):


        if fecha == datetime.date.today().strftime('%Y%m%d'):
            texto = "#Conteo parcial de menciones a palabras relacionadas con " + self.hashtags[concepto] + " del " + self.separar_fecha(fecha) + " 📊\n"
        else:
            texto = "#Conteo final de menciones a palabras relacionadas con " + self.hashtags[concepto] + " del " + self.separar_fecha(fecha) + " 📊\n"

        i = 0
        for diario, m in freqs.items():
            linea = ""
            i += 1
            if i >= 10:
                linea = str(i) + ". " + self.hashtags[diario] + ": " + str(m) + "\n"
                texto += linea
                break
            else:
                linea = str(i) + ".  " + self.hashtags[diario] + ": " + str(m) + "\n"

            if len(texto) + len(linea) > 220:
                break
            else:
                texto += linea

        return texto

    def tweet_tendencias(self, freqs, fecha, diario, secciones=None):
        texto = ""
        if secciones:
            if type(secciones) is list:
                hashtags_secciones = ["#"+s for s in secciones]

                if len(secciones) > 0:
                    secciones = " de " + " y ".join([", ".join(hashtags_secciones[:-1]),hashtags_secciones[-1]] if len(hashtags_secciones) > 2 else hashtags_secciones)
            else:
                secciones = '#' + secciones

            texto = "#Frecuencia de palabras en los textos de " + secciones + " de " + self.hashtags[diario] + " del " + self.separar_fecha(fecha) + " 📊\n"
        else:
            texto = "📊 #Frecuencia de palabras en los textos de " + self.hashtags[diario] + " del " + self.separar_fecha(fecha=fecha) + ". Hilo 👇\n"
        
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

        return texto

    def texto_tweet_sustantivos_discurso(self, freqs):
        texto = "#Frecuencia de sustantivos 📊\n"

        i = 0
        for nombre, m in freqs.items():
            linea = ""
            i += 1
            if i >= 10:
                linea = str(i) + ". #" + nombre + " " + str(m) + "\n"
                texto += linea
                break
            else:
                linea = str(i) + ".  #" + nombre + " " + str(m) + "\n"

            if len(texto) + len(linea) > 220:
                break
            else:
                texto += linea

        return texto

    def texto_tweet_verbos_discurso(self, freqs):
        texto = "#Frecuencia de verbos 📊\n"

        i = 0
        for nombre, m in freqs.items():
            linea = ""
            i += 1
            if i >= 10:
                linea = str(i) + ". #" + nombre + " " + str(m) + "\n"
                texto += linea
                break
            else:
                linea = str(i) + ".  #" + nombre + " " + str(m) + "\n"

            if len(texto) + len(linea) > 220:
                break
            else:
                texto += linea

        return texto

    def texto_tweet_adjetivos_discurso(self, freqs):
        texto = "#Frecuencia de adjetivos 📊\n"

        i = 0
        for nombre, m in freqs.items():
            linea = ""
            i += 1
            if i >= 10:
                linea = str(i) + ". #" + nombre + " " + str(m) + "\n"
                texto += linea
                break
            else:
                linea = str(i) + ".  #" + nombre + " " + str(m) + "\n"

            if len(texto) + len(linea) > 220:
                break
            else:
                texto += linea

        return texto

    def separar_fecha(self, fecha, separador='.'):
        if type(fecha) is str:
            return fecha[6:8] + separador + fecha[4:6] + separador + fecha[0:4]