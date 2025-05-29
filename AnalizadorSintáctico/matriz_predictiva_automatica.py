import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AnalizadorSintáctico.GeneradorEstructurasGramatica import GeneradorEstructurasGramatica


class FirstFollowMatrix:


    def __init__(self):
        self.estructuras = GeneradorEstructurasGramatica()
        self.estructuras.crearEstructuras()
        self.gramatica = self.estructuras.getGramatica()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.first = [[]] # Conjunto First (primeros simbolos, numero de produccion)
        self.follow = [] # Conjunto Follow para cada no terminal
        self.matrix = [[]]  # Matriz predictiva
   
    def stripCadena(self, cadena):
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1
        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1
    
        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
    
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1

    def dividirSimbolos(self, cadena):
        """
        Divide una cadena en símbolos separados por espacios, aplicando stripCadena a cada uno.
        Equivalente a cadena.split() pero controlado.
        """
        partes = []
        simbolo = ''
        for c in cadena:
            if c.isspace():
                if simbolo:
                    partes.append(self.stripCadena(simbolo))
                    simbolo = ''
            else:
                simbolo += c
        if simbolo:
            partes.append(self.stripCadena(simbolo))
        return partes

    # Verificar si el primer símbolo de una derivación es un terminal
    def esTerminal(self, simbolo):
        return self.stripCadena(simbolo) in self.terminales
    
    # Verificar si el símbolo de una derivación es un no terminal
    def esNoTerminal(self, simbolo):
        return self.stripCadena(simbolo) in self.noterminales
    
    # Verificar si el símbolo de una derivación es vacío
    def esVacio(self, simbolo):
        return self.stripCadena(simbolo) == '&'
    
    # Calcula los conjuntos FIRST para todos los no terminales de la gramática.
    def calcularFirst(self):
        producciones = {}
        for i in range(len(self.noterminales)):
            no_terminles = self.noterminales[i]
            producciones[no_terminles] = []

        for i in range(len(self.gramatica)):
            lado_izquierdo = self.stripCadena(self.estructuras.leerNoTerminales(self.gramatica[i][1]))
            lado_derecho = self.stripCadena(self.estructuras.leerDerivacion(self.gramatica[i][1]))
            producciones[lado_izquierdo].append(self.dividirSimbolos(lado_derecho))

        FIRST = {nt: set() for nt in self.noterminales}
        cambio = True
        while cambio:
            cambio = False
            for nt in self.noterminales:
                for prod in producciones[nt]:
                    for simbolo in prod:
                        simbolo = self.stripCadena(simbolo)
                        if simbolo in self.terminales:
                            if simbolo not in FIRST[nt]:
                                FIRST[nt].add(simbolo)
                                cambio = True
                            break
                        elif simbolo in self.noterminales:
                            tam_antes = len(FIRST[nt])
                            FIRST[nt].update(FIRST[simbolo] - {'ε'})
                            if 'ε' not in FIRST[simbolo]:
                                break
                            if len(FIRST[nt]) > tam_antes:
                                cambio = True
                        elif simbolo == 'ε':
                            if 'ε' not in FIRST[nt]:
                                FIRST[nt].add('ε')
                                cambio = True
                            break
        self.first = FIRST
    
    # Calcula los conjuntos FOLLOW para todos los no terminales
    def calcularFollow(self):
        producciones = {}
        for i in range(len(self.noterminales)):
            nt = self.noterminales[i]
            producciones[nt] = []

        for i in range(len(self.gramatica)):
            lado_izq = self.stripCadena(self.estructuras.leerNoTerminales(self.gramatica[i][1]))
            lado_der = self.stripCadena(self.estructuras.leerDerivacion(self.gramatica[i][1]))
            producciones[lado_izq].append(self.dividirSimbolos(lado_der))

        FOLLOW = {nt: set() for nt in self.noterminales}
        simbolo_inicial = self.noterminales[0]
        FOLLOW[simbolo_inicial].add('$')
        cambio = True
        while cambio:
            cambio = False
            for nt in self.noterminales:
                for prod in producciones[nt]:
                    for i, simbolo in enumerate(prod):
                        simbolo = self.stripCadena(simbolo)
                        if simbolo in self.noterminales:
                            siguiente = prod[i+1:]
                            first_siguiente = set()
                            for s in siguiente:
                                s = self.stripCadena(s)
                                if s in self.terminales:
                                    first_siguiente.add(s)
                                    break
                                elif s in self.noterminales:
                                    first_siguiente.update(self.first[s] - {'ε'})
                                    if 'ε' not in self.first[s]:
                                        break
                                elif s == 'ε':
                                    first_siguiente.add('ε')
                                    break
                            else:
                                first_siguiente.add('ε')

                            tam_antes = len(FOLLOW[simbolo])
                            FOLLOW[simbolo].update(first_siguiente - {'ε'})
                            if 'ε' in first_siguiente or not siguiente:
                                FOLLOW[simbolo].update(FOLLOW[nt])
                            if len(FOLLOW[simbolo]) > tam_antes:
                                cambio = True
        self.follow = FOLLOW
    
    # Construye la matriz predictiva LL(1) a partir de los conjuntos FIRST y FOLLOW.
    def calcularMatriz(self):
        self.matrix = [[None for _ in self.terminales + ['$']] for _ in self.noterminales]
        for i, produccion in enumerate(self.gramatica):
            linea, regla = produccion
            nt = self.stripCadena(self.estructuras.leerNoTerminales(regla))
            lado_der = self.dividirSimbolos(self.estructuras.leerDerivacion(regla))
            simbolos_first = set()

            for simbolo in lado_der:
                simbolo = self.stripCadena(simbolo)
                if simbolo in self.terminales:
                    simbolos_first.add(simbolo)
                    break
                elif simbolo in self.noterminales:
                    simbolos_first.update(self.first[simbolo] - {'ε'})
                    if 'ε' not in self.first[simbolo]:
                        break
                elif simbolo == 'ε':
                    simbolos_first.add('ε')
                    break
            else:
                simbolos_first.add('ε')

            for terminal in simbolos_first:
                if terminal != 'ε':
                    fila = self.noterminales.index(nt)
                    columna = self.terminales.index(terminal)
                    self.matrix[fila][columna] = linea

            if 'ε' in simbolos_first:
                for terminal in self.follow[nt]:
                    fila = self.noterminales.index(nt)
                    if terminal == '$':
                        columna = len(self.terminales)  # última columna
                    else:
                        columna = self.terminales.index(terminal)
                    self.matrix[fila][columna] = linea

            # Reemplazar todos los None por 0
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    if self.matrix[i][j] is None:
                        self.matrix[i][j] = 0


    def main(self):
        self.calcularFirst()
        self.calcularFollow()
        self.calcularMatriz()
        print("First:")
        for k, v in self.first.items():
            print(f"{k}: {v}")
        print("\nFollow:")
        for k, v in self.follow.items():
            print(f"{k}: {v}")
        print("\nMatriz Predictiva:")
        for fila in self.matrix:
            print(fila)


if __name__ == "__main__":
    FirstFollowMatrix().main()
