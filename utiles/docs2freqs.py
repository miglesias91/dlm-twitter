from nltk import word_tokenize, bigrams

class docs2freqs:

    def __init__(self, docs):
        self.docs = docs

        self.stopwords = []
        with open('stopwords.txt') as s:
           self.stopwords = s.read().split('\n')

        self.sustantivos_comunes = []
        with open('sustantivos.txt') as s:
           self.sustantivos_comunes = s.read().split('\n')

        import string

        self.puntuacion = string.punctuation + "¡¿\n"

        self.freqs = {}


    def calcular(self):
        
        i = 1
        print(f'docs a procesar: {len(self.docs)}')
        for doc in self.docs:

            print(f'procesando doc: {i}')
            i += 1
            
            doc = doc.lower().translate(str.maketrans('', '', self.puntuacion))
            terminos = word_tokenize(doc)
            
            terminos = [t.strip() for t in terminos if t.translate(str.maketrans('áéíóúý', 'aeiouy')) not in self.sustantivos_comunes and t.translate(str.maketrans('áéíóúý', 'aeiouy')) not in self.stopwords]
            bigramas = ["_".join(list(bigrama)) for bigrama in list(bigrams(terminos))]

            tokens = terminos + bigramas
            for token in tokens:

                if len(token) < 5 or len(token) > 20:
                    continue

                if token.isdigit() and len(token) != 4:
                    continue

                token_sin_tildes = token.translate(str.maketrans('áéíóúý', 'aeiouy'))
                if token_sin_tildes in self.sustantivos_comunes or token_sin_tildes in self.stopwords:
                    continue

                if token not in self.freqs:
                    self.freqs[token] = 0

                self.freqs[token] += 1

    def top_sin_duplicados(self, top):

        ranking = {k: v for k, v in sorted(self.freqs.items(), key=lambda item: item[1], reverse=True)}

        # rescato los bigramas
        bigramas_tops = []
        i = 0
        for t, f in ranking.items():
            i += 1
            if i >= top + 15:
                break
            if '_' in t:
                bigramas_tops.extend(t.split('_'))

        # rescato los unigramas que terminan el s (posibles plurales)
        # y creo una lista con las posibilidades de plurar de los unigramas singulares
        posibles_plurales = []
        unigramas_tops_plurales = []
        freqs_tops_plurales = []
        i = 0
        for t, f in ranking.items():
            i += 1
            if i >= top + 15:
                break
            if '_' not in t and t[-1] != 's':
                posibles_plurales.append(t + 's')
                posibles_plurales.append(t + 'as')
                posibles_plurales.append(t + 'es')
                posibles_plurales.append(t + 'is')
                posibles_plurales.append(t + 'os')
                posibles_plurales.append(t + 'us')
            
            if '_' not in t and t[-1] == 's':
                unigramas_tops_plurales.append(t)
                freqs_tops_plurales.append(f)


        # descarto los unigramas que: o estan dentro de bigramas, o están dentro de un unigrama
        topfinal = {}
        i = 1
        for t, f in ranking.items():
            
            # si no es parte de un bigrama y no es posible plurar
            if '_' not in t and t not in bigramas_tops and t not in posibles_plurales:

                freq_del_plural = self._tiene_plural(t, unigramas_tops_plurales, freqs_tops_plurales)

                if freq_del_plural:
                    f += freq_del_plural

                topfinal[t] = f
                i += 1

            # formateo como hashtag el bigrama
            if '_' in t:
                bigrama = ''.join([s.capitalize() for s in t.split('_')])
                topfinal[bigrama] = f
                i += 1

            if i >= top:
                break
        
        return {k: v for k, v in sorted(topfinal.items(), key=lambda item: item[1], reverse=True)}

    def _tiene_plural(self, singular, plurales, freqs_plurales):

        sufijos = ['s', 'as', 'es', 'is', 'os', 'us']

        for sufijo in sufijos:
            if singular + sufijo in plurales:
                return freqs_plurales[plurales.index(singular + sufijo)]
        return 0