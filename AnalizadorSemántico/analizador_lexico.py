import os
# Módulo que contiene los AFNs para diferentes tipos de tokens
import AFN
# Módulo que contiene la clase Pila (estructura tipo stack)
import pila as stack

# Clase principal que implementa un analizador léxico utilizando AFNs.
class AnalizadorLexico:


    def __init__(self, nombre_archivo="AnalizadorSemántico/programa_ejemplo_6.txt"):
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


    def generar_tabla_simbolos(self, tabla_tokens: dict, tokens_linea: list) -> dict:
        """
        Construye la tabla de símbolos a partir de la tabla de tokens.
        Incluye solo identificadores y constantes
        """

        tabla_simbolos = {}
        errores = []
        id_token_actual = 500
        i = 0

        while i < len(tokens_linea):
            token = tokens_linea[i][0] # Ubicación del lexema

            # Detectar declaraciones de variables
            if token.lower() in ["float", "int"]:
                tipo_var = "float" if token.lower() == "float" else "int"
                i += 1

                # Recorrer hasta encontrar ';'
                while i < len(tokens_linea) and tokens_linea[i][0] != ";":
                    var_token, _ = tokens_linea[i]

                    if var_token not in [",", "=", ";"]:
                        if var_token in tabla_tokens and tabla_tokens[var_token]["tipo"] == "Identificador": # Nos aseguramos de que este en la tabla de tokens
                            if var_token not in tabla_simbolos:
                                tabla_simbolos[var_token] = {
                                    "tipo": tipo_var,
                                    "id_token": id_token_actual,
                                    "repeticiones": tabla_tokens[var_token]["repeticiones"],
                                    "lineas": tabla_tokens[var_token]["lineas"],
                                    "valor": "0.0" if tipo_var == "float" else "0"
                                }
                            else:
                                # Error de redeclaración
                                errores.append({
                                    "variable": var_token,
                                    "linea": tokens_linea[i][1],
                                    "tipo_anterior": tabla_simbolos[var_token]["tipo"],
                                    "tipo_nuevo": tipo_var
                                })
                            id_token_actual += 1

                    # Si hay asignación (=) después del identificador
                    if i + 2 < len(tokens_linea) and tokens_linea[i+1][0] == "=":
                        valor = tokens_linea[i+2][0]
                        if var_token in tabla_simbolos:
                            tabla_simbolos[var_token]["valor"] = valor
                            
                    i += 1
            else:
                i += 1

        # Ahora agregamos las constantes literales (enteros y relaes)
        for token, info in tabla_tokens.items():
            if info["tipo"] in ["Número Real", "Número Entero"]:
                if token not in tabla_simbolos:
                    tabla_simbolos[token] = {
                        "tipo": "int" if info["tipo"] == "Número Entero" else "float",
                        "id_token": "",
                        "repeticiones": info["repeticiones"],
                        "lineas": info["lineas"],
                        "valor": token
                    }

        return tabla_simbolos, errores


    def distribuir_tokens_en_tablas(self):
        # Definimos la ruta y nombre del archivo
        ruta_carpeta = "AnalizadorSemántico"
        archivo_salida = "resultados_lexicos.txt"
        ruta_completa = os.path.join(ruta_carpeta, archivo_salida)

        tabla_tokens = {}
        tokens_linea = []
        # Abre el archivo 'resultados_lexicos.txt' en modo escritura ('w')
        # para guardar los resultados del análisis léxico.
        with open(ruta_completa, 'w') as salida:
            salida.write("Archivo Tabla de Tokens\n")

            # Recorre la pila de tokens mientras no esté vacía.
            while self.pila_tokens:
                # Extrae un token desde la pila (tipo pila LIFO)
                resultado = self.pila_tokens.popDat()
                if resultado is None:
                    break # Sale del ciclo si no hay más tokens

                # Desempaqueta el token y su número de línea
                token, linea = resultado
                tokens_linea.append((token, linea))

                # Determina el tipo léxico del token (identificador, número, palabra reservada, etc.)
                tipo = self.clasificar_token(token)
                # Obtiene el atributo asociado al token (puede ser un valor numérico o textual)
                atributo = self.obtener_atributo(token, tipo)

                # Clasificación y almacenamiento de los tokens
                if tipo not in ["Error Léxico"]:
                    if token not in tabla_tokens: 
                        tabla_tokens[token] = {
                            "tipo": tipo,
                            "atributo": atributo,
                            "repeticiones": 1,
                            "lineas": [linea]
                        }
                    else:
                        # Actualizamos la información
                        tabla_tokens[token]["repeticiones"] += 1
                        tabla_tokens[token]["lineas"].append(linea)

            tokens_linea.reverse() # Porque era pila LIFO

            # Guardar la tabla de tokens    
            salida.write("\nTabla de Tokens:\n")
            for token, info in tabla_tokens.items():
                lineas_string = ", ".join(map(str, info['lineas']))
                salida.write(f"| {token:<15} | Tipo: {info['tipo']:<20} | Atributo: {info['atributo']:<6} | Linea: {lineas_string:<5}\n")

            # Construir la tabla de símbolos a partir de la tabla de tokens
            tabla_simbolos, errores = self.generar_tabla_simbolos(tabla_tokens, tokens_linea)

            salida.write("\nTabla de Símbolos:\n")
            for simbolo, info in tabla_simbolos.items():
                lineas_string = ", ".join(map(str, info['lineas']))
                salida.write(f"| {simbolo:<15} | Tipo: {info['tipo']:<20} | id_token: {info['id_token']:<6} | Repeticiones: {info['repeticiones']:<3} | Linea: {lineas_string:<20} | valor: {info["valor"]}\n")
            if errores:
                salida.write("\nTabla de Errores:\n")
                for err in errores:
                    salida.write(f"| Variable: {err['variable']:<10} | Línea: {err['linea']:<3} | Declarada antes como {err['tipo_anterior']} y ahora como {err['tipo_nuevo']} |\n")

        # Devolvemos las estructuras para usarlas en otros fragmentos de código
        return tabla_tokens, tokens_linea, tabla_simbolos, errores

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
    analizador_lexico = AnalizadorLexico()

    

