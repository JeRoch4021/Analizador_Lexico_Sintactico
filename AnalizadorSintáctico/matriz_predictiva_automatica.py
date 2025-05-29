import GeneradorEstructurasG as ges

class FirstFollowMatrix:
    def __init__(self):
        self.estructuras = ges.GeneradorEstructurasG()
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

    # Verificar si el primer símbolo de una derivación es un terminal
    def esTerminal(self, simbolo):
        return self.stripCadena(simbolo) in self.terminales
    
    # Verificar si el símbolo de una derivación es un no terminal
    def esNoTerminal(self, simbolo):
        return self.stripCadena(simbolo) in self.noterminales
    
    # Verificar si el símbolo de una derivación es vacío
    def esVacio(self, simbolo):
        return self.stripCadena(simbolo) == '&'
    
    def calcularFollow(self):
        # Implementación del cálculo de Follow
        pass
    
    def calcularMatriz(self):
        # Código para calcular la matriz predictiva
        pass
    
    def calcular_first(producciones, terminales, no_terminales):
        FIRST = {nt: set() for nt in no_terminales}
        cambio = True
        while cambio:
            cambio = False
            for nt in no_terminales:
                for prod in producciones[nt]:
                    for simbolo in prod:
                        if simbolo in terminales:
                            if simbolo not in FIRST[nt]:
                                FIRST[nt].add(simbolo)
                                cambio = True
                            break
                        elif simbolo in no_terminales:
                            antes = len(FIRST[nt])
                            FIRST[nt].update(FIRST[simbolo] - {"ε"})
                            if "ε" not in FIRST[simbolo]:
                                break
                            if len(FIRST[nt]) > antes:
                                cambio = True
                        elif simbolo == "ε":
                            if "ε" not in FIRST[nt]:
                                FIRST[nt].add("ε")
                                cambio = True
                            break
        return FIRST
    
    
    def calcular_follow(producciones, terminales, no_terminales, first, simbolo_inicial):
        FOLLOW = {nt: set() for nt in no_terminales}
        FOLLOW[simbolo_inicial].add("$")
        cambio = True
        while cambio:
            cambio = False
            for nt in no_terminales:
                for prod in producciones[nt]:
                    for i, simbolo in enumerate(prod):
                        if simbolo in no_terminales:
                            siguiente = prod[i+1:] if i+1 < len(prod) else []
                            first_siguiente = set()
                            for s in siguiente:
                                if s in terminales:
                                    first_siguiente.add(s)
                                    break
                                elif s in no_terminales:
                                    first_siguiente.update(first[s] - {"ε"})
                                    if "ε" not in first[s]:
                                        break
                                elif s == "ε":
                                    first_siguiente.add("ε")
                                    break
                            else:
                                first_siguiente.add("ε")
                            antes = len(FOLLOW[simbolo])
                            FOLLOW[simbolo].update(first_siguiente - {"ε"})
                            if "ε" in first_siguiente or not siguiente:
                                FOLLOW[simbolo].update(FOLLOW[nt])
                            if len(FOLLOW[simbolo]) > antes:
                                cambio = True
        return FOLLOW

    def main(self):
        self.calcularFirst()
        self.calcularFollow()
        self.calcularMatriz()
        print("First:", self.first)
        print("Follow:", self.follow)
        print("Matriz Predictiva:", self.matrix)

if __name__ == "__main__":
    FirstFollowMatrix().main()
