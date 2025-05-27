import os
# Módulo que contiene los AFNs para diferentes tipos de tokens
from . import AFN
# Módulo que contiene la clase Pila (estructura tipo stack)
from . import pila as stack
# import analizador_sintactico as prueba

# Clase principal que implementa un analizador léxico utilizando AFNs.
class AnalizadorLexico:


    def __init__(self, nombre_archivo="AnalizadorLexico/programa.txt"):
        # Inicialización de los AFNs para reconocer diferentes tipos de tokens
        self.afn_identificador = AFN.crear_afn_identificador()
        self.afn_binario = AFN.crear_afn_binario()
        self.afn_octal = AFN.crear_afn_octal()
        self.afn_hexadecimal = AFN.crear_afn_hexadecimal()
        self.afn_caracter_simple = AFN.crear_afn_caracter_simple()
        # Pila para almacenar los tokens encontrados
        self.pila_tokens = stack.Pila()
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
        self.tokens = []
        self.indice_token = 0
        self.cargar_tokens(nombre_archivo)
        self.analizar_archivo(nombre_archivo)
        self.distribuir_tokens_en_tablas()


    def cargar_tokens(self, nombre_archivo):
        if not os.path.exists(nombre_archivo):
            print("Archivo no encontrado.")
            return
        with open (nombre_archivo, 'r') as archivo:
            numero_linea = 1
            for linea in archivo:
                palabras = self.obtener_palabras_de_cadena(self.stripCadena(linea))

                for palabra in palabras:
                    self.tokens.append(palabra)

                numero_linea += 1


    def scanner(self):
        # Devuelve el siguiente token del archivo fuente
        if self.indice_token < len(self.tokens):
            token = self.tokens[self.indice_token]
            self.indice_token += 1
            return token 
        else:
            return None


    def obtener_palabras_de_cadena(self, cadena: str) -> list:
        # Separa una cadena continua en tokens, reconociendo caracteres simples y espacios.
        palabras = []
        palabra = []
        i = 0
        longitud = len(cadena)

        while i < longitud:
            caracter = cadena[i]

            # Si hay espacio o carácter simple, finaliza token anterior y guarda el símbolo
            if caracter.isspace() or self.es_caracter_simple(caracter):
                if palabra:
                    subcadena = "".join(palabra)
                    palabras.extend(self.procesar_subcadena(subcadena))
                    palabra = []
                if self.es_caracter_simple(caracter):
                    palabras.append(caracter)
                i += 1
                continue

            palabra.append(caracter)
            i += 1
        # Procesar la última palabra si queda algo
        if palabra:
            subcadena = "".join(palabra)
            palabras.extend(self.procesar_subcadena(subcadena))

        return palabras
    

    def procesar_subcadena(self, cadena: str) -> list:
        # Divide una subcadena continua en múltiples tokens válidos (máximo prefijo válido).
        palabras = []
        inicio = 0
        longitud = len(cadena)

        while inicio < longitud:
            final = inicio + 1
            ultimo_token_valido = None
            ultima_pos_valida = inicio

            while final <= longitud:
                subcadena = cadena[inicio:final]
                tipo = self.clasificar_token(subcadena)
                if tipo != 'Error Lexico':
                    ultimo_token_valido = subcadena
                    ultima_pos_valida = final
                final += 1

            if ultimo_token_valido:
                palabras.append(ultimo_token_valido)
                inicio = ultima_pos_valida
            else:
                final = inicio + 1
                while final < longitud and self.clasificar_token(cadena[inicio:final + 1]) == 'Error Lexico':
                    final += 1
                palabras.append(cadena[inicio:final])
                inicio = final

        return palabras
    

    def es_caracter_simple(self, caracter: str) -> bool:
        # Verifica si un carácter es un símbolo reconocido por el AFN de caracteres simples
        return self.afn_caracter_simple.procesar(caracter)


    def clasificar_token(self, token: str) -> str:
        # Clasifica un token usando los AFNs disponibles y palabras reservadas
        match True:
            case _ if token in AFN.palabras_reservadas:
                return 'Palabra Reservada'
            case _ if self.afn_identificador.procesar(token):
                return 'Identificador'
            case _ if self.afn_binario.procesar(token):
                return 'Numero Binario'
            case _ if self.afn_octal.procesar(token):
                return 'Numero Octal'
            case _ if self.afn_hexadecimal.procesar(token):
                return 'Numero Hexadecimal'
            case _ if self.afn_caracter_simple.procesar(token):
                return 'Caracter Simple'
            case _:
                return 'Error Lexico'


    def obtener_atributo(self, token: str, tipo: str) -> int:
         # Devuelve el valor numérico del atributo para cada tipo de token
        match tipo:
            case 'Palabra Reservada':
                return self.atributos_reservados.get(token, 0)
            case 'Identificador':
                return 261
            case 'Numero Binario':
                return 520
            case 'Numero Octal':
                return 732
            case 'Numero Hexadecimal':
                return 891
            case 'Caracter Simple':
                return ord(token)
            case _ :
                return 0
    
    
    def analizar_archivo(self, nombre_archivo: str) -> str:
        # Analiza línea por línea un archivo de texto para extraer y clasificar tokens
        if not os.path.exists(nombre_archivo):
            print("Archivo no encontrado.")
            return
        
        print("\nAbriendo Programa.txt")
        with open(nombre_archivo, 'r') as archivo:
            numero_linea = 1
            for linea in archivo:
                print(f"\nAnalizando línea {numero_linea}: {self.stripCadena(linea)}")

                # Aquí entra el analizador sintáctico
                # Método para extraer palabras/tokens
                palabras = self.obtener_palabras_de_cadena(self.stripCadena(linea))

                for palabra in palabras:
                    self.pila_tokens.push((palabra, numero_linea))

                numero_linea += 1
        print()

    def distribuir_tokens_en_tablas(self):
        tabla_simbolos = []
        tabla_palabras_reservadas = []
        # Abre el archivo 'resultados_lexicos.txt' en modo escritura ('w')
        # para guardar los resultados del análisis léxico.
        with open("resultados_lexicos.txt", 'w') as salida:
            salida.write("Resultados del Análisis Léxico\n")

            # Recorre la pila de tokens mientras no esté vacía.
            while self.pila_tokens:
                # Extrae un token desde la pila (tipo pila LIFO)
                resultado = self.pila_tokens.popDat()
                if resultado is not None:
                    # Desempaqueta el token y su número de línea
                    token, _ = resultado
                else:
                    break # Sale del ciclo si no hay más tokens
                
                # Determina el tipo léxico del token (identificador, número, palabra reservada, etc.)
                tipo = self.clasificar_token(token)
                # Obtiene el atributo asociado al token (puede ser un valor numérico o textual)
                atributo = self.obtener_atributo(token, tipo)

                 # Clasificación y almacenamiento de los tokens en sus tablas correspondientes
                if tipo == 'Identificador' and (token, atributo) not in tabla_simbolos:
                    tabla_simbolos.append((token, atributo))
                    # tabla_tokens_validos.append((token, atributo, linea, tipo))
                if tipo == 'Palabra Reservada' and (token, atributo) not in tabla_palabras_reservadas:
                    tabla_palabras_reservadas.append((token, atributo))

            # Guardado de resultados en archivo de salida
            salida.write("\nTabla de Símbolos:\n")
            for simbolo, atributo in sorted(tabla_simbolos):
                salida.write(f"| {simbolo:<15} | Atributo: {atributo:<6} |\n")

            salida.write("\nTabla de Palabras Reservadas:\n")
            for palabra, atributo in sorted(tabla_palabras_reservadas):
                salida.write(f"| {palabra:<15} | Atributo: {atributo:<6} |\n")
    

    # Elimina los espacios en blanco de una cadena
    def stripCadena(self, cadena: str) -> str:
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1

        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1

        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
        
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1 

