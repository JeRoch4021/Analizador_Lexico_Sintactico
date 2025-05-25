from AnalizadorLexico.analizador_lexico import AnalizadorLexico
from AnalizadorSintáctico.analizador_sintactico import AnaliadorSintactico

if __name__ == "__main__":
    lexico = AnalizadorLexico()
    lexico.main_analizador_lexico()
    sintactico = AnaliadorSintactico(lexico)
    print()
    sintactico.imprimir_tokens()