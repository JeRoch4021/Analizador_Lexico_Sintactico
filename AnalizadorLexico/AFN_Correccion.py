class automata:
    def __init__(self):
        self.estado = 0
         # Diccionario con palabras reservadas y sus atributos únicos
        self.atributos_reservados = {
            'programa': 257, 
            'binario': 258, 
            'octal': 259, 
            'hexad': 260, 
            'leer': 265, 
            'escribir': 262, 
            'finprograma': 263
        }
        # Identificadores: Token 270
        # Números Binarios: Token 271
        # Números Octales: Token 272
        # Números Hexadecimales: Token 273
        # Caracteres Simples: Token ASCII  
    
    def transiciones(self, estado, simbolo: str) -> str | None:
        inicio = 0
        fin = len(simbolo) - 1
        match estado:
            case 0:
                if simbolo[inicio] in '01' and simbolo[fin] == 'B':
                    estado = 1
                return estado
            case 1:

                return None
            case 2:
                return None
            case 3:
                return None
            case 4:
                return None
            case 5:
                return None
            case 6:
                return None
            case 7:
                return None
            case 8:
                return None
            case 9:
                if simbolo[inicio] in '':
                return None
            case 10:
                return 'Error Lexico'
            
    def generarToken(self, numero: int) -> str:
        if numero in self.atributos_reservados:
            return "Palabra Reservada"
        elif numero == 270:
            return "Identificador"
        elif numero == 271:
            return "Número Binario"
        elif numero == 272:
            return "Número Octal"
        elif numero == 273:
            return "Número Hexadecimal"
        elif numero in ";=+-*()/,":
            return "Carácter Simple"
        else:
            return "Error Lexico"
