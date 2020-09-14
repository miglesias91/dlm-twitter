import datetime

from wordcloud import WordCloud as wc

class Visualizador:
    def __init__(self):
        pass

    def nube(self, path, freqs, con_espacios=True):
        if not con_espacios:
            aux = freqs
            freqs = {}
            for k,v in aux.items():
                freqs[k.replace(' ','')] = v

        wordcloud = wc(width=1280,height=720,background_color="black",colormap=self.cmap_del_dia(),min_font_size=14,prefer_horizontal=1,relative_scaling=1).generate_from_frequencies(freqs)
        wordcloud.recolor(100)
        wordcloud.to_file(path)

    def texto_en_imagenes(self, texto, font_path, font_tam, anchomax, altomax, nombre_imagen, modo='RGBA', color_texto=(0,0,0,0), color_fondo=(255,255,255,255) ,xy=(5,5)):
        textos_por_imagen = []
        font = ImageFont.truetype(font_path, font_tam)
        
        if font.getsize(texto)[0] <= anchomax:
            textos_por_imagen.append(texto)
        else:
            palabras = texto.split(' ')
            i = 0
            while i < len(palabras):
                texto = ''
                altura = font.getsize(texto + palabras[i])[1]
                while i < len(palabras) and altura <= altomax:
                    linea = ''
                    while i < len(palabras) and font.getsize(linea + palabras[i] + " ")[0] <= anchomax:
                        if palabras[i] != "\n":
                            linea = linea + palabras[i]+  " "
                            i += 1
                        else:
                            i += 1
                            break
                    if not linea:
                        linea = palabras[i]
                        i += 1
                    texto = texto + linea + '\n'
                    altura += font.getsize(texto)[1] + 2

                textos_por_imagen.append(texto)

        i = 0
        paths = []
        x, y = xy
        for texto in textos_por_imagen:
            img = Image.new(modo, (anchomax, altomax), color_fondo)
            dibujo = ImageDraw.Draw(img)
            dibujo.text((x,y), texto, font=font, fill=color_texto)
            path = nombre_imagen + str(i) + ".png"
            img.save(path)
            paths.append(path)
            i += 1

        return paths

    def cmap_del_dia(self):
        cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
                
        hoy = datetime.datetime.now()
        idx = (hoy.year + hoy.month + hoy.day) % len(cmaps)

        return cmaps[idx]