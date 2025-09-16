import os
# Módulo que contiene los AFNs para diferentes tipos de tokens
import AFN
# Módulo que contiene la clase Pila (estructura tipo stack)
import pila as stack

# Clase principal que implementa un analizador léxico utilizando AFNs.
class AnalizadorLexico:


    def __init__(self, nombre_archivo="AnalizadorSemántico/programa_ejemplo_1.txt"):
        self.automata_transiciones = AFN.automata()
        # Pila para almacenar los tokens encontrados
        self.pila_tokens = stack.Pila()
         # Diccionario con palabras reservadas y sus atributos únicos
        self.atributos_reservados = {
            'programa': 257, 
            'int': 258, 
            'float': 259,
            'leer': 265, 
            'escribir': 262, 
            'finprograma': 263
        }
        self.tokens = []
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
            ultimo_token_vacio = None
            ultima_posicion_valida = inicio

            while final <= longitud:
                subcadena = cadena[inicio:final]
                tipo = self.clasificar_token(subcadena)
                if tipo != 'Error Léxico':
                    # Si la subcadena completa es un token valido, lo guardamos como valido
                    return [cadena]
                else:
                    # Si no es un token valido, lo guardamos como error léxico
                    return [cadena]

        return palabras
    

    def es_caracter_simple(self, caracter: str) -> bool:
        # Verifica si un carácter es un símbolo reconocido por el AFN de caracteres simples
        return caracter in '()*+,-/;'


    def clasificar_token(self, token: str) -> str:
        # Clasifica un token usando los AFNs disponibles y palabras reservadas
        estado = self.automata_transiciones.transiciones(0, token)
        tipo = self.automata_transiciones.transiciones(estado, token)
        return tipo


    def obtener_atributo(self, token: str, tipo: str) -> int:
         # Devuelve el valor numérico del atributo para cada tipo de token
        match tipo:
            case 'Palabra Reservada':
                return self.atributos_reservados.get(token, 0)
            case 'Identificador':
                return 261
            case 'Caracter Simple':
                return ord(token)
            case 'Asignación':
                return 520
            case 'Operador Aritmético':
                return ord(token)
            case 'Número Entero':
                return 732
            case 'Número Real':
                return 891
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

                # Método para extraer palabras/tokens
                palabras = self.obtener_palabras_de_cadena(self.stripCadena(linea))

                for palabra in palabras:
                    self.pila_tokens.push((palabra, numero_linea))

                numero_linea += 1
        print()


    def distribuir_tokens_en_tablas(self):
        # Definimos la ruta y nombre del archivo
        ruta_carpeta = "AnalizadorSemántico"
        archivo_salida = "resultados_lexicos.txt"
        ruta_completa = os.path.join(ruta_carpeta, archivo_salida)

        tabla_tokens = {}
        # Abre el archivo 'resultados_lexicos.txt' en modo escritura ('w')
        # para guardar los resultados del análisis léxico.
        with open(ruta_completa, 'w') as salida:
            salida.write("Archivo Tabla de Tokens\n")

            # Recorre la pila de tokens mientras no esté vacía.
            while self.pila_tokens:
                # Extrae un token desde la pila (tipo pila LIFO)
                resultado = self.pila_tokens.popDat()
                if resultado is not None:
                    # Desempaqueta el token y su número de línea
                    token, linea = resultado
                else:
                    break # Sale del ciclo si no hay más tokens
                
                # Determina el tipo léxico del token (identificador, número, palabra reservada, etc.)
                tipo = self.clasificar_token(token)
                # Obtiene el atributo asociado al token (puede ser un valor numérico o textual)
                atributo = self.obtener_atributo(token, tipo)

                # Clasificación y almacenamiento de los tokens
                if tipo not in ["Error Léxico"]:
                    if token not in tabla_tokens: 
                        tabla_tokens[token]={
                            "tipo": tipo,
                            "atributo": atributo,
                            "repeticiones": 1,
                            "lineas": [linea]
                        }
                    else:
                        # Actualizamos la información
                        tabla_tokens[token]["repeticiones"] += 1
                        tabla_tokens[token]["lineas"].append(linea)
                
            salida.write("\nTabla de Tokens:\n")
            for token, info in tabla_tokens.items():
                lineas_string = ", ".join(map(str, info['lineas']))
                salida.write(f"| {token:<15} | Tipo: {info['tipo']:<20} | Atributo: {info['atributo']:<6} | Linea: {lineas_string:<5}\n")
    

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
    
if __name__ == "__main__":
    analizasor_lexico = AnalizadorLexico()