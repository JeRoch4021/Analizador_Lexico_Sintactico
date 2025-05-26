import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#import AnalizadorLexico as al
from AnalizadorLexico.analizador_lexico import AnalizadorLexico
#import GeneradorEstructurasGramatica as gen
from AnalizadorSintáctico.GeneradorEstructurasGramatica import GeneradorEstructurasGramatica
#import Pila as p
from Pila.Pila import Pila
#import AnalizadorLexico as lexico


class AnalizadorSintactico:
    def __init__(self):
        # Inicializa el analizador léxico
        #self.analizador_lexico = lexico.AnalizadorLexico()
        self.analizador_lexico = AnalizadorLexico()
        #self.pila = p.Pila()
        self.pila = Pila()
        self.token_actual = None
        self.estructuras = GeneradorEstructurasGramatica()
        self.estructuras.crearEstructuras()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.matrizPredictiva = self.estructuras.getMatrizPredictiva()

    # def imprimir_tokens(self):
    #     while True:
    #         token = self.analizador_lexico.scanner()  # Obtener el siguiente token del analizador léxico
    #         if token is None:
    #             break
    #         print(token)

    def LlDriver(self):
        self.pila.push(self.noterminales[0])  # Agregar el símbolo inicial a la pila
        x = self.pila.peek() # Actualiza x con el símbolo en la parte superior de la pila
        a = self.analizador_lexico.scanner()  # Obtener el token de entrada del analizador léxico
        while self.pila.isEmpty() == False:
            x = self.pila.peek()  # Actualiza x con el símbolo en la parte superior de la pila
            if x in self.noterminales:
                predict = self.obtenerProduccion(x, a)  # Obtiene la producción correspondiente
                if predict != 0:
                    x = self.derivaciones[predict-1]
                    self.pila.pop()
                    self.cicloPush(self.stripCadena(x)) # Agrega los símbolos de la derivación a la pila
                else:
                    self.procesarErrorSintactico(a)
                    break # Detiene el ciclo despues de procesar el error
            else:
                if self.coinciden(x, a) or x == a:
                    self.pila.pop()
                    a = self.analizador_lexico.scanner()
                else:
                    self.procesarErrorSintactico(a)
                    break # Detiene el ciclo despues de procesar el error
            print("Pila actual: ", self.pila)

    def obtenerProduccion(self, x, a):
        # Obtiene la produccion correspondiente a un no termianl (x) y un terminal (a)
        if x in self.noterminales and a in self.terminales:
            i = self.noterminales.index(x)
            j = self.terminales.index(a)
            return self.matrizPredictiva[i][j]
        return 0


    # Método para meter los simbolos de las derivaciones a la pila
    def cicloPush(self, x):
        print("Derivación: ", x)
        cursor1 = len(x)
        cursor2 = len(x)
        while cursor1 >= 0:
            if x[cursor1-1] == " " or cursor1 == 0:  # Verifica si es un espacio o el inicio de la cadena
                print("metiendo a la pila: ", x[cursor1:cursor2])
                self.pila.push(self.stripCadena(x[cursor1:cursor2]))  # Agrega el símbolo a la pila
                cursor2 = cursor1  # Actualiza el cursor2 al inicio del siguiente símbolo
            cursor1 -= 1
    
    def coinciden(self, x, a):
        # Verifica si la parte superior de la pila (x) coincide con el token actual (a) en cuanto a clasificación lexica
        clasificacionA = self.analizador_lexico.clasificar_token(a)
        print(a," Clasificación del token actual: ", clasificacionA," | Símbolo en la pila - {x}: ", x)
        if clasificacionA == 'Identificador' and x == 'id':
            return True
        elif clasificacionA == 'Numero Binario' and x == 'litbinaria':
            return True
        elif clasificacionA == 'Numero Octal' and x == 'litoctal':
            return True
        elif clasificacionA == 'Numero Hexadecimal' and x == 'lithexadecimal':
            return True
        else:
            return False


    def procesarErrorSintactico(self, token):
        print(f"Error sintáctico: token inesperado '{token}'")
        self.pila.pop()  # Ignorar el token inesperado
    

    def stripCadena(self, cadena: str) -> str:
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1

        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1

        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
        
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1 


    def main(self):
        print()
        # Imprime la gramática, derivaciones, no terminales y terminales
        self.estructuras.printGramatica()
        print()
        self.estructuras.printDerivacion()
        print()
        self.estructuras.printNoTerminales()
        print()
        self.estructuras.printTerminales()
        print()
        self.estructuras.printMatrizPredictiva()
        print()
        # Inicia el análisis sintáctico
        self.LlDriver()


# if __name__ == "__main__":
#     # Crea una instancia del analizador léxico
#     analizador_lexico = AnalizadorLexico()
#     # Crea una instancia del analizador sintáctico 
#     analizador_sintactico = AnalizadorSintactico()
#     # Llama al método principal del analizador sintáctico
#     analizador_sintactico.main()
