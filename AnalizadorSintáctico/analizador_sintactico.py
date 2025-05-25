import AnalizadorLexico as al
import GeneradorEstructurasG as gen
import Pila as p
import AnalizadorLexico as lexico

class AnalizadorSintactico:
    def __init__(self):
        # Inicializa el analizador léxico
        self.analizador_lexico = lexico.AnalizadorLexico()
        self.pila = p.Pila()
        self.token_actual = None
        self.estructuras = gen.GeneradorEstructurasG()
        self.estructuras.crearEstructuras()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.matrizPredictiva = self.estructuras.getMatrizPredictiva()

    def imprimir_tokens(self):
        while True:
            token = self.analizador_lexico.scanner()  # Obtener el siguiente token del analizador léxico
            if token is None:
                break
            print(token)

    def LlDriver(self):
        self.pila.push(self.noterminales[0])  # Agregar el símbolo inicial a la pila
        x = self.pila.peek()  # Obtener el símbolo en la parte superior de la pila
        a = self.analizador_lexico.scanner()  # Obtener el token de entrada del analizador léxico
        while self.pila.isEmpty() == False:
            if x in self.noterminales:
                if self.matrizPredictiva[self.noterminales.index(x)][self.terminales.index(a)] != 0:
                    x = self.derivaciones[self.matrizPredictiva[self.noterminales.index(x)][self.terminales.index(a)]-1]
                    self.pila.pop()
                    self.cicloPush(x)
                    a = self.analizador_lexico.scanner()
                else:
                    self.procesarErrorSintactico(a)
                    a = self.analizador_lexico.scanner()
            else:
                if x == a:
                    self.pila.pop()
                    a = self.analizador_lexico.scanner()
                else:
                    self.procesarErrorSintactico(a)
                    a = self.analizador_lexico.scanner()

    # Método para meter los simbolos de las derivaciones a la pila
    def cicloPush(self, x):
        cursorDer = len(x)-1
        simbolo = ""
        while cursorDer >= 0:
            if x[cursorDer] == " ":
                self.pila.push(simbolo[::-1])  # Invertir el símbolo antes de agregarlo a la pila
                simbolo = ""
            else:
                simbolo += x[cursorDer]
            cursorDer -= 1
        print("Pila: ", self.pila)

    def procesarErrorSintactico(self, token):
        print(f"Error sintáctico: token inesperado '{token}'")
        self.pila.pop()  # Ignorar el token inesperado

    def main(self):
        # Imprime la gramática, derivaciones, no terminales y terminales
        self.estructuras.printGramatica()
        self.estructuras.printDerivacion()
        self.estructuras.printNoTerminales()
        self.estructuras.printTerminales()
        self.estructuras.printMatrizPredictiva()
        # Inicia el análisis sintáctico
        self.LlDriver()

if __name__ == "__main__":
    # Crea una instancia del analizador léxico
    analizador_lexico = al.AnalizadorLexico()
    # Crea una instancia del analizador sintáctico 
    analizador_sintactico = AnalizadorSintactico()
    # Llama al método principal del analizador sintáctico
    analizador_sintactico.main()
