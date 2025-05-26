#from AnalizadorLexico.analizador_lexico import AnalizadorLexico
from AnalizadorSintáctico.analizador_sintactico import AnalizadorSintactico

if __name__ == "__main__":
    # # Crea una instancia del analizador léxico
    # analizador_lexico = AnalizadorLexico()
    # Crea una instancia del analizador sintáctico 
    analizador_sintactico = AnalizadorSintactico()
    # Llama al método principal del analizador sintáctico
    analizador_sintactico.main()