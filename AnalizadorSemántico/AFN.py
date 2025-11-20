from pila import Pila  
class automata:
    def __init__(self):
        self.estado = 0
        self.listaExpresionesPrefijas=[]

         # Diccionario con palabras reservadas y sus atributos únicos
        self.atributos_reservados = {
            'programa': 257, 
            'int': 258, 
            'float': 259,
            'leer': 265, 
            'escribir': 262,
            'mostrar' : 263,
            'finprograma': 264
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
                partes = self.splitCadena(simbolo, '.')
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

    def splitCadena(self, cadena: str, caracter) -> list:
        # Divide una cadena en una lista usando un carácter separador específico
        partes = []
        palabra = []
        for char in cadena:
            if char == caracter:
                if palabra:
                    partes.append("".join(palabra))
                    palabra = []
            else:
                palabra.append(char)
        if palabra:
            partes.append("".join(palabra))
        return partes

    def precedencia(self, operador: str) -> int:
        if operador in ('+', '-'):
            return 1
        elif operador in ('*', '/'):
            return 2
        return 0

    def conversionPrefija(self, tokens: list[str]) -> list[str]:
        pila = Pila()
        resultado = []
        operadores = set(['+', '-', '*', '/', '='])
        
        for token in reversed(tokens):
            if token in operadores:
                while (not pila.isEmpty() and pila.peek() in operadores 
                    and self.precedencia(token) < self.precedencia(pila.peek())):
                    resultado.append(pila.pop())
                pila.push(token)
            else:
                resultado.append(token)
        while not pila.isEmpty():
            resultado.append(pila.pop())
        return resultado[::-1]  # lista de tokens prefija
    
    def comprobar_asignacion(self, expresion: str, tabla_simbolos: dict) -> bool:
        """
        Verifica la validez de una asignación con comprobación de tipos.
        """

        # 1) Separamos lado izquierdo y derecho
        if '=' not in expresion:
            print("Error: no es una asignación válida")
            return False
        var_izq, expr_der = [parte.strip() for parte in expresion.split('=', 1)]

        # 2) Validamos que la variable de la izquierda exista en la tabla
        if var_izq not in tabla_simbolos:
            print(f"Error: variable '{var_izq}' no declarada en tabla de símbolos")
            return False
        tipo_izq = tabla_simbolos[var_izq]

        # 3) Convertimos la parte derecha a prefija (tokenizada)
        tokens_der = expr_der.split()  # convertir string a lista de tokens
        expr_prefija = self.conversionPrefija(tokens_der)
        print(f"Prefija derecha: {expr_prefija}")

        # 4) Comprobamos tipos en la parte derecha
        tipo_derecha = self.comprobar_tipos(expr_prefija, tabla_simbolos)
        if tipo_derecha is None:
            return False  # error detectado

        # 5) Comprobamos compatibilidad de asignación
        if tipo_izq == tipo_derecha:
            print(f"Asignación válida: {var_izq} ({tipo_izq}) = expr ({tipo_derecha})")
            return True
        elif tipo_izq == "float" and tipo_derecha == "int":
            print(f"Asignación válida con promoción: {var_izq} ({tipo_izq}) = expr ({tipo_derecha})")
            return True
        else:
            print(f"Error de tipos en asignación: {var_izq} ({tipo_izq}) = expr ({tipo_derecha})")
            return False

        
    def comprobar_tipos(self, expresion_prefija: list[str], tabla_simbolos: dict) -> str | None:
        """
        Verifica la expresión prefija y devuelve el tipo resultante si es válido.
        :return: 'int', 'float' o None si hubo error
        """
        pila_tipos = []
        operadores = {'+', '-', '*', '/'}
        tokens = expresion_prefija  # ya es lista de tokens

        for token in reversed(tokens):
            if token in operadores:
                if len(pila_tipos) < 2:
                    print(f"Error: faltan operandos para {token}")
                    return None
                tipo1 = pila_tipos.pop()
                tipo2 = pila_tipos.pop()

                if tipo1 == tipo2:
                    pila_tipos.append(tipo1)
                elif (tipo1, tipo2) in [('int', 'float'), ('float', 'int')]:
                    pila_tipos.append('float')
                else:
                    print(f"Error de tipos: {tipo1} {token} {tipo2}")
                    return None
            else:
                if token in tabla_simbolos:
                    pila_tipos.append(tabla_simbolos[token])
                elif token.isdigit():
                    pila_tipos.append('int')
                elif '.' in token and token.replace('.', '').isdigit():
                    pila_tipos.append('float')
                else:
                    print(f"Error: token {token} no reconocido")
                    return None

        return pila_tipos[0] if len(pila_tipos) == 1 else None

    
if __name__ == "__main__":
    afn = automata()
    expresion = "a + b * c - d / e"
    tokens = expresion.split()  # divide por espacios
    prefija = afn.conversionPrefija(tokens)
    print(prefija)

    tabla_simbolos = {
    'a': 'int',
    'b': 'float',
    'c': 'int',
    'd': 'float',
    'e': 'int'
}
    expresion = "c = a + b * 3"
    resultado = afn.comprobar_asignacion(expresion, tabla_simbolos)
    print("Resultado de la asignación:", resultado)

