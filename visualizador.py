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

    def cmap_del_dia(self):
        cmaps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
                
        hoy = datetime.datetime.now()
        idx = (hoy.year + hoy.month + hoy.day) % len(cmaps)

        return cmaps[idx]