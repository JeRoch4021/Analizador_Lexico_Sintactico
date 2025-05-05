import os
from collections import deque
import AFN

class AnalizadorLexico:


    def __init__(self):
        self.afn_identificador = AFN.crear_afn_identificador()
        self.afn_binario = AFN.crear_afn_binario()
        self.afn_octal = AFN.crear_afn_octal()
        self.afn_hexadecimal = AFN.crear_afn_hexadecimal()
        self.afn_caracter_simple = AFN.crear_afn_caracter_simple()
        self.pila_tokens = deque()
        self.atributos_reseervados = {
            'programa': 257, 
            'binario': 258, 
            'octal': 259, 
            'hexadecimal': 260, 
            'leer': 265, 
            'escribir': 262, 
            'finprograma': 263
        }

    def es_caracter_simple(self, caracter: str) -> bool:
        return self.afn_caracter_simple.procesar(caracter)


    def leer_por_linea_de_texto(self, linea_texto: str) -> list:
        cadenas = linea_texto.split()
        palabras = []

        for cadena in cadenas:
            palabras_en_cadena = self.obtener_palabras_de_cadena(cadena)
            palabras.extend(palabras_en_cadena)

        return palabras


    def obtener_palabras_de_cadena(self, cadena: str) -> list:
        palabras = []
        palabra = []

        if not cadena or len(cadena.strip()) == 0:
            return palabras

        for caracter in cadena:
            if caracter.isspace() or self.es_caracter_simple(caracter):
                if palabra:
                    palabras.append("".join(palabra))
                    palabra = []

                if self.es_caracter_simple(caracter):
                    palabras.append(caracter)
            else:
                palabra.append(caracter)

        if palabra:
            palabras.append("".join(palabra))

        return palabras
    

    def clasificar_token(self, token: str) -> str:
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
        match tipo:
            case 'Palabra Reservada':
                return self.atributos_reseervados.get(token, 0)
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


    def analizar_archivo(self, nombre_archivo: str):
        if not os.path.exists(nombre_archivo):
            print("Archivo no encontrado.")
            return

        tabla_simbolos = set()
        tabla_palabras_reservadas = set()
        tabla_tokens_validos = []
        tabla_errores = []

        with open(nombre_archivo, 'r') as archivo:
            numero_linea = 1
            for linea in archivo:
                print(f"\nAnalizando línea {numero_linea}: {linea.strip()}")

                # Método para extraer palabras/tokens
                palabras = self.leer_por_linea_de_texto(linea.strip())

                for palabra in palabras:
                    self.pila_tokens.append((palabra, numero_linea))

                numero_linea += 1
        # Linea de espacio
        print("\n\nObtención de Tokens:\n")
        with open("resultados_lexicos.txt", 'w') as salida:
            salida.write("Resultados del Análisis Léxico\n\n")
            salida.write("Tokens Clasificados:\n")

            while self.pila_tokens:
                token, linea = self.pila_tokens.popleft()
                tipo = self.clasificar_token(token)
                atributo = self.obtener_atributo(token, tipo)
                print(f"({token}, atributo {atributo}, {tipo}, línea {linea})")
                salida.write(f"({token}, atributo {atributo}, {tipo}, línea {linea})\n")

                if tipo == 'Identificador':
                    tabla_simbolos.add(token)
                    tabla_tokens_validos.append((token, atributo, linea, tipo))
                elif tipo == 'Palabra Reservada':
                    tabla_palabras_reservadas.add(token)
                    tabla_tokens_validos.append((token, atributo, linea, tipo))
                elif tipo.startswith("Numero") or tipo == 'Caracter Simple':
                    tabla_tokens_validos.append((token, atributo, linea, tipo))
                else:
                    tabla_errores.append((token, linea))

            salida.write("\nTabla de Símbolos:\n")
            for simbolo in sorted(tabla_simbolos):
                salida.write(f"{simbolo}\n")

            salida.write("\nTabla de Palabras Reservadas:\n")
            for palabra in sorted(tabla_palabras_reservadas):
                salida.write(f"{palabra}\n")

            salida.write("\nTabla de Tokens Válidos:\n")
            for token,  atributo, linea, tipo in tabla_tokens_validos:
                salida.write(f"{token}   Atributo: {atributo}   {tipo}, Línea {linea}\n")

            salida.write("\nTabla de Errores Léxicos:\n")
            for token, linea in tabla_errores:
                salida.write(f"{token}   Línea {linea}\n")

        print("\nAnálisis completado. Resultados guardados en 'resultados_lexicos.txt'.")


if __name__ == "__main__":
    analizador = AnalizadorLexico()
    analizador.analizar_archivo("CodigoAnalizadorLexico/programa.txt")