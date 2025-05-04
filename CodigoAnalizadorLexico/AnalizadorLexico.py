# Código para modelar el AFN del analizador léxico
# Código para modelar el AFN del analizador léxico
import re
import ListaDobleEnlazada as lista_tokens

class AnalizadorLexico:
    def __init__(self, estados, simbolos, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.simbolos = simbolos
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.palabras_reservadas = {'programa', 257}, {'binario', 258}, {'octal', 258}, {'hexadecimal', 259}, {'leer', 260}, {'escribir', 261}, {'finprograma', 262}

    # Determina si el simbpolo es un identificador
    def esLetraMinuscula(self, simbolo):
        return re.match(r'[a-z]', simbolo) is not None # devuelve True si el simbolo es una letra minuscula

    # Determina si el simbolo es un digito entre 0 y 9
    def esNumero(self, simbolo):
        return simbolo in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    
    # Determina si el simbolo es un digito hexadecimal
    def esHexadecimal(self, simbolo):
        return simbolo in {'A', 'B', 'C', 'D', 'E', 'F'} or self.esNumero(simbolo)
    
    # Determina si el simbolo es un caracter simple
    def esCaracterSimple(self, simbolo):
        return simbolo in { ';', '=', '+', '-', '/', '*', ',', '(' , ')'}
    
    # Determina si el simbolo es un digito binario
    def esBinario(self, simbolo):
        return simbolo in {0,1}
    
    # Genera un token y lo agrega a la lista de tokens
    def generarToken(self, identificador):
        lista_tokens.ListaEnlazada().agregar(identificador) # Agrega el token a la lista de tokens


    def switch(self, estado):
        match estado:
            case 1:
                return 2
            case 2:
                return 3
            case 3:
                return 4
            case 4:
                return 5
            case 5:
                return 6
