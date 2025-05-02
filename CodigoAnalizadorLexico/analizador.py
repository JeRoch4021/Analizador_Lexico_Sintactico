import re

class AnalizadorLexico:
    def __init__(self):
        self.reglas = {
            'palabra_reservada': r'\b(programa|binario|octal|hexadecimal|leer|escribir|finprograma)\b',
            'identificador': r'\b[a-z]+\b',
            'binario': r'\b[01]+B\b',
            'octal': r'\b[0-7]+O\b',
            'hexadecimal': r'\b[0-9A-F]+X\b',
            'caracter_simple': r'[;=+\-/*,()]',
        }
        self.tokens = []
        self.errores = []
        self.simbolos = set()
        self.reservadas = set()

    def limpiar(self):
        self.tokens.clear()
        self.errores.clear()
        self.simbolos.clear()
        self.reservadas.clear()

    def analizar_contenido(self, texto):
        self.limpiar()
        for num_linea, linea in enumerate(texto.splitlines(), 1):
            tokens = re.findall(r'\b\w+\b|[;=+\-/*,()]', linea)
            for token in tokens:
                clasificado = False
                for tipo, patron in self.reglas.items():
                    if re.fullmatch(patron, token):
                        self.tokens.append((token, tipo, num_linea))
                        if tipo == 'palabra_reservada':
                            self.reservadas.add(token)
                        elif tipo == 'identificador':
                            self.simbolos.add(token)
                        clasificado = True
                        break
                if not clasificado:
                    self.errores.append((token, num_linea))

    def obtener_reporte(self):
        return {
            'tokens': self.tokens,
            'reservadas': sorted(self.reservadas),
            'simbolos': sorted(self.simbolos),
            'errores': self.errores,
        }