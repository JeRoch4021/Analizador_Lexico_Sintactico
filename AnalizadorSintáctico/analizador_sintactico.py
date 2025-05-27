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
        self.analizador_lexico = al.AnalizadorLexico()
        #self.pila = p.Pila()
        self.pila = p.Pila()
        self.token_actual = None
        self.estructuras = gen.GeneradorEstructurasG()
        self.estructuras.crearEstructuras()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.matrizPredictiva = self.estructuras.getMatrizPredictiva()

    def LlDriver(self):
        self.pila.push(self.noterminales[0])  # Agregar el símbolo inicial a la pila
        x = self.pila.peek() # Actualiza x con el símbolo en la parte superior de la pila
        a = self.analizador_lexico.scanner()  # Obtener el token de entrada del analizador léxico
        while self.pila.isEmpty() == False:
            print("\tSímbolo en la parte superior de la pila (x): ", x)
            print("\tToken actual (a): ", a)
            if x in self.noterminales:
                predict = self.obtenerProduccion(x, a)  # Obtiene la producción correspondiente
                print("\tDerivación obtenida: ", str(predict))
                if predict != 0:
                    x = self.derivaciones[predict-1] # Obtiene la cadena de derivación
                    self.pila.pop()
                    self.cicloPush(self.stripCadena(x)) # Agrega los símbolos de la derivación a la pila
                else:
                    self.procesarErrorSintactico(a)
                    break  # Sale del ciclo si hay un error sintáctico
            else:
                if self.coinciden(x, a) or x == a:
                    self.pila.pop()
                    a = self.analizador_lexico.scanner()
                else:
                    self.procesarErrorSintactico(a)
                    break  # Sale del ciclo si hay un error sintáctico
            print("Pila actual: ", self.pila)
            if self.pila.isEmpty() == False: 
                x = self.stripCadena(self.pila.peek())  # Actualiza x con el símbolo en la parte superior de la pila

    def obtenerProduccion(self, x, a):
        # Obtiene la produccion correspondiente a un no termianl (x) y un terminal (a)
        term = self.obtenerClasificacion(a)
        if x in self.noterminales and term in self.terminales:
            i = self.noterminales.index(x)
            j = self.terminales.index(term)
            print("Posición en la matriz: ", str(i),", ", str(j))
            return self.matrizPredictiva[i][j]
        return 0


    # Método para meter los simbolos de las derivaciones a la pila
    def cicloPush(self, x):
        print("\t\tDerivación: ", x)
        cursor1 = len(x)
        cursor2 = len(x)
        while cursor1 >= 0:
            if x[cursor1-1] == " " or cursor1 == 0:  # Verifica si es un espacio o el inicio de la cadena
                if self.stripCadena(x[cursor1:cursor2]) != "&": # Si no es la cadena vacía
                    print("\tmetiendo a la pila: ", x[cursor1:cursor2])
                    self.pila.push(self.stripCadena(x[cursor1:cursor2]))  # Agrega el símbolo a la pila
                cursor2 = cursor1  # Actualiza el cursor2 al inicio del siguiente símbolo
            cursor1 -= 1

    def obtenerClasificacion(self, token):
        # Obtiene la clasificación léxica del token
        clasificacionA = self.analizador_lexico.clasificar_token(token)
        if clasificacionA == 'Identificador':
            return 'id'
        elif clasificacionA == 'Numero Binario':
            return 'litbinaria'
        elif clasificacionA == 'Numero Octal':
            return 'litoctal'
        elif clasificacionA == 'Numero Hexadecimal':
            return 'lithexadecimal'
        return token  # Retorna el token tal cual si no es un identificador o número
    
    def coinciden(self, x, a):
        # Verifica si la parte superior de la pila (x) coincide con el token actual (a) en cuanto a clasificación lexica
        clasificacionA = self.analizador_lexico.clasificar_token(a)
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
