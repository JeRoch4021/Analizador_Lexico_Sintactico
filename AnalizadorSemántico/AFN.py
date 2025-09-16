class automata:
    def __init__(self):
        self.estado = 0

         # Diccionario con palabras reservadas y sus atributos únicos
        self.atributos_reservados = {
            'programa': 257, 
            'int': 258, 
            'float': 259,
            'leer': 265, 
            'escribir': 262, 
            'finprograma': 263
        }

        # Identificadores: Token 261
        self.letras = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Conjunto de simbolos especiales
        # Caracteres Simples: Token ASCII
        self.simbolos_especiales = {
            '(',
            ')',
            '*',
            '+',
            ',',
            '-',
            '/',
            ';'
        }

        # Conjunto de asignación
        # Asignación: Token 520
        self.asignacion = {'='}

        # Uso de diccionarios para  operaciones aritmeticas
        self.operaciones_aritmeticas = {
            '+': 521,
            '-': 522,
            '*': 523,
            '/': 524
        }
        
        # Conjunto de numeros enteros
        self.digitos_enteros = set("0123456789")
    
    def transiciones(self, estado: int, simbolo: str) -> str | None:
        inicio = 0
        fin = len(simbolo) - 1
        match estado:
            case 0:
                if simbolo in self.atributos_reservados: # Palabras reservadas
                    estado = 7
                elif simbolo[inicio] in self.letras: # Identificadores
                    estado = 1
                elif simbolo[inicio] in self.asignacion: # Asignación 
                    estado = 2
                elif simbolo in self.operaciones_aritmeticas: # Operadores aritmeticos
                    estado = 3
                elif simbolo[inicio] in self.digitos_enteros: # Números enteros
                    # Si contiene un punto --> Es un número real
                    if "." in simbolo:
                        estado = 5
                    else:
                        estado = 4
                elif simbolo[inicio] in self.simbolos_especiales: # Simbolos especiales
                    estado = 6
                else: # Error léxico
                    estado = 8
                return estado
            case 1:
                while inicio < fin:
                    if simbolo[inicio] in self.letras:
                        inicio += 1
                    else:
                        estado = 8  # Error Léxico
                        return estado
                return self.generarToken(261)  # Identificador
            case 2:
                return self.generarToken(520)  # Asignación
            case 3:
                return self.generarToken(self.operaciones_aritmeticas[simbolo]) # Operadores Aritmeticos
            case 4:
                while inicio < fin:
                    if simbolo[inicio] in self.digitos_enteros:
                        inicio += 1
                    else:
                        estado = 8  # Error Léxico
                        return estado
                return self.generarToken(732)  # Numeros enteros
            case 5:
                partes = simbolo.split(".")
                if len(partes) == 2 and all(p.isdigit() for p in partes if p):
                    return self.generarToken(891)  # Numeros reales
                else:
                    estado = 8  # Error Léxico
                    return estado
            case 6:
                return self.generarToken(ord(simbolo[inicio]))  # Carácter Simple
            case 7:
                return self.generarToken(self.atributos_reservados[simbolo]) # Palabra Reservada
            case 8:
                return self.generarToken(0) # Error Léxico
            
    def generarToken(self, numero: int) -> str:
        if numero in self.atributos_reservados.values():
            return "Palabra Reservada"
        elif numero == 261:
            return "Identificador"
        elif numero in range(39, 62):
            return "Caracter Simple"
        elif numero == 520:
            return "Asignación"
        elif numero in self.operaciones_aritmeticas.values():
            return "Operador Aritmético"
        elif numero == 732:
            return "Número Entero"
        elif numero == 891:
            return "Número Real"
        else:
            return "Error Léxico"