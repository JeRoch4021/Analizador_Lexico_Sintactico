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
        # Identificadores: Token 261
        # Números Binarios: Token 520
        # Números Octales: Token 732
        # Números Hexadecimales: Token 891
        # Caracteres Simples: Token ASCII  
    
    def transiciones(self, estado: int, simbolo: str) -> str | None:
        inicio = 0
        fin = len(simbolo) - 1
        match estado:
            case 0:
                if simbolo in self.atributos_reservados:
                    estado = 6
                elif simbolo[inicio] in '01' and simbolo[fin] == 'B':
                    estado = 1
                elif simbolo[inicio] in '01234567' and simbolo[fin] == 'O':
                    estado = 2
                elif simbolo[inicio] in '0123456789ABCDEF' and simbolo[fin] == 'X':
                    estado = 3
                elif simbolo[inicio] in 'abcdefghijklmnopqrstuvwxyz':
                    estado = 4
                elif simbolo[inicio] in '()*+,-/;=':
                    estado = 5
                else:
                    estado = 7
                return estado
            case 1:
                while inicio < fin:
                    if simbolo[inicio] in '01':
                        inicio += 1
                    else:
                        estado = 7 # Error Lexico
                        return estado
                return self.generarToken(520)  # Número Binario
            case 2:
                while inicio < fin:
                    if simbolo[inicio] in '01234567':
                        inicio += 1
                    else:
                        estado = 7  # Error Lexico
                        return estado
                return self.generarToken(732)  # Número Octal
            case 3:
                while inicio < fin:
                    if simbolo[inicio] in '0123456789ABCDEF':
                        inicio += 1
                    else:
                        estado = 7 # Error Lexico
                        return estado
                return self.generarToken(891)  # Número Hexadecimal
            case 4:
                while inicio < fin:
                    if simbolo[inicio] in 'abcdefghijklmnopqrstuvwxyz':
                        inicio += 1
                    else:
                        estado = 7  # Error Lexico
                        return estado
                return self.generarToken(261)  # Identificador
            case 5:
                return self.generarToken(ord(simbolo[inicio]))  # Carácter Simple
            case 6:
                return self.generarToken(self.atributos_reservados[simbolo]) # Palabra Reservada
            case 7:
                return self.generarToken(0) # Error Lexico
            
    def generarToken(self, numero: int) -> str:
        if numero in self.atributos_reservados.values():
            return "Palabra Reservada"
        elif numero == 261:
            return "Identificador"
        elif numero == 520:
            return "Número Binario"
        elif numero == 732:
            return "Número Octal"
        elif numero == 891:
            return "Número Hexadecimal"
        elif numero in range(39, 62):
            return "Carácter Simple"
        else:
            return "Error Lexico"
