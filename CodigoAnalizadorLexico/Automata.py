# Código para modelar el AFN del analizador léxico
import re

class Automata:
    def __init__(self, estados, simbolos, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.simbolos = simbolos
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

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
            
    def esLetraMinuscula(self, simbolo):
        return re.match(r'[a-z]', simbolo) is not None # devuelve True si el simbolo es una letra minuscula

    def esNumero(self, simbolo):
        return simbolo in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    
    def esCaracterSimple(self, simbolo):
        return simbolo in { ';', '=', '+', '-', '/', '*', ',', '(' , ')'}
    
    def esBinario(self, simbolo):
        return simbolo in {0,1}
