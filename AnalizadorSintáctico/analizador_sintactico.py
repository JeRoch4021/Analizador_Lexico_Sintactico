import AnalizadorLexico as al
import GeneradorEstructurasG as gen
import Pila as p

class AnalizadorSintactico:
    def __init__(self, analizador_lexico):
        self.analizador_lexico = analizador_lexico
        self.pila = p.Pila()
        self.token_actual = None
        self.estructuras = gen.GeneradorEstructurasG()
        self.estructuras.crearEstructuras()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.matrizPredictiva = {[1, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 2,0, 0,0,2,0, 0,2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 3,4, 0,0,3,0, 0,3, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
                                 [0, 6,0, 0,0,7,0, 0,8, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
                                 [0, 9,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0,0,11,0,0,0,11,0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0,12,0, 0,0,0,0, 0,0, 0,12,12,12, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0,0,14,0,0,0,14,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0,0, 0,0,0,0, 0,0, 0,16,17,18, 0, 0, 0,13,13,13,13],
                                 [0, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0,19,20,21, 0, 0, 0, 0],
                                 [0, 0,0, 0,0,0,0, 0,0, 0, 0, 0, 0, 0, 0, 0,22,23,25,24]}

    def LlDriver(self):
        self.pila.push(self.noterminales[0])  # Agregar el símbolo inicial a la pila
        x = self.pila.peek()  # Obtener el símbolo en la parte superior de la pila
        a = self.analizador_lexico.scanner()  # Obtener el token de entrada del analizador léxico
        while self.pila.isEmpty() == False:
            if x in self.noterminales:
                if self.matrizPredictiva[x,a] != 0:
                    x = self.derivaciones[self.matrizPredictiva[x,a]-1]
                    self.pila.pop()
                    self.cicloPush(x)
                else:
                    self.procesarErrorSintactico()
            else:
                if x == a:
                    self.pila.pop()
                    a = self.analizador_lexico.scanner()
                else:
                    self.procesarErrorSintactico()

    # Método para meter los simbolos de las derivaciones a la pila
    def cicloPush(self, x):
        cursorDer = len(x)-1
        simbolo = ""
        while cursorDer >= 0:
            if x[cursorDer] != " ":
                simbolo += x[cursorDer]
            else:
                self.pila.push(simbolo[cursorDer+1:len(simbolo)])
                simbolo = ""
            cursorDer -= 1

    def procesarErrorSintactico(self):
        print(f"Error sintáctico: token inesperado '{token}'")
        # Aquí puedes agregar más lógica para manejar el error, como registrar el error o intentar recuperarse.
        # Por ejemplo, podrías intentar ignorar el token y continuar con el análisis.
        # self.pila.pop()  # Ignorar el token inesperado
        # self.token_actual = self.analizador_lexico.scanner()  # Obtener el siguiente token

class AnaliadorSintactico:
    def __init__(self, lexico):
        self.lexico = lexico
    
    def imprimir_tokens(self):
        while True:
            token = self.lexico.scanner()
            if token is None:
                break
            print(token)

    
    
