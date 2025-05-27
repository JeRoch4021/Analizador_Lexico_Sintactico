from AnalizadorSintáctico.analizador_sintactico import AnalizadorSintactico
class main:
    def __init__(self):
        self.analizador_sintactico = AnalizadorSintactico()
    
    def run(self):
        self.analizador_sintactico.main()

if __name__ == "__main__":
    main().run()
