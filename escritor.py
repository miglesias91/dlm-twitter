

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
            'todonoticias': '#TN'
        }

    def tweet_tendencias(self, freqs, fecha, diario, categorias=None):

        texto = ""
        if categorias:
            if type(categorias) is list:
                hashtags_categorias = ["#"+c for c in categorias]

                if len(categorias) > 0:
                    secciones = " de " + " y ".join([", ".join(hashtags_categorias[:-1]),hashtags_categorias[-1]] if len(hashtags_categorias) > 2 else hashtags_categorias)
            else:
                secciones = '#' + categorias

            texto = "Tendencias en las noticias de " + secciones + " de " + self.hashtags[diario] + " del " + self.separar_fecha(fecha) + "\n"
        else:
            texto = "Tendencias en las noticias " + self.hashtags[diario] + " del " + self.separar_fecha(fecha=fecha) + "\n"
        
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

    def separar_fecha(self, fecha, separador='.'):
        if type(fecha) is str:
            return fecha[0:4] + separador + fecha[4:6] + separador + fecha[6:8]