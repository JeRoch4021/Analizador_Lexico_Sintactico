import GeneradorEstructurasG as ges

class FirstFollowMatrix:
    def __init__(self):
        self.estructuras = ges.GeneradorEstructurasG()
        self.estructuras.crearEstructuras()
        self.gramatica = self.estructuras.getGramatica()
        self.derivaciones = self.estructuras.getDerivaciones()
        self.noterminales = self.estructuras.getNoTerminales()
        self.terminales = self.estructuras.getTerminales()
        self.first = [] # Conjunto First (primeros simbolos, numero de produccion)
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

    def calcularFirst(self):
        # Implementación del cálculo de First para cada no terminal
        for no_terminal in self.noterminales:
            self.first.append((no_terminal, [])) # Inicializa el conjunto First para cada no terminal

        for i in range(len(self.derivaciones)):
            no_terminal = self.stripCadena(self.obtenerNoTerminal(self.gramatica[i][1]))  # Obtiene el no terminal de la derivación
            simbolo = self.stripCadena(self.obtenerPrimerSimbolo(self.derivaciones[i]))  # Obtiene el primer símbolo de la derivación
            if self.esTerminal(simbolo) or self.esVacio(simbolo):
                # Si el símbolo es un terminal, lo añadimos directamente al conjunto First
                for first in self.first: # Recorre el conjunto First
                    if first[0] == no_terminal: # Busca el no terminal correspondiente
                        first[1].append(simbolo) # Añade el terminal al conjunto First
        
        for i in range(len(self.derivaciones) - 1, -1, -1):
            no_terminal = self.stripCadena(self.obtenerNoTerminal(self.gramatica[i][1]))  # Obtiene el no terminal de la derivación
            simbolo = self.stripCadena(self.obtenerPrimerSimbolo(self.derivaciones[i]))  # Obtiene el primer símbolo de la derivación
            if self.esNoTerminal(simbolo):
                # Si el símbolo es un no terminal añadimos sus First al conjunto del no terminal correspondiente
                for first in self.first: # Recorre el conjunto First
                    if first[0] == no_terminal: # Busca el no terminal correspondiente
                        # Buscar First(simbolo)
                        simbolos_origen = []
                        for nt, simbolos in self.first:
                            if nt == simbolo:
                                simbolos_origen = simbolos
                                break

                        # Agregar a First(no_terminal), evitando duplicados
                        for j, (nt, simbolos_destino) in enumerate(self.first):
                            if nt == no_terminal:
                                for s in simbolos_origen:
                                    if s not in simbolos_destino:
                                        simbolos_destino.append(s)
                                break
                    
    def calcularFollow(self):
        # Implementación del cálculo de Follow para cada no terminal
        for no_terminal in self.noterminales:
            self.follow.append((no_terminal, []))
        
        for i in range(len(self.derivaciones)):
            produccion = self.stripCadena(self.derivaciones[i])  # Obtiene la producción de la derivación
            lado_izquierdo = self.stripCadena(self.obtenerNoTerminal(self.gramatica[i][1]))  # Obtiene el lado izquierdo de la producción
            simbolos = self.obtenerSimbolos(produccion)  # Obtiene los símbolos de la producción
            print(f"Símbolos: {simbolos}")
            for j in range(len(simbolos)):
                if self.esNoTerminal(simbolos[j]) and j < len(simbolos) - 1:
                    if self.esTerminal(simbolos[j + 1]):
                        # Si el siguiente símbolo es un terminal, lo añadimos al Follow del no terminal
                        for follow in self.follow:
                            if follow[0] == simbolos[j] and simbolos[j + 1] not in follow[1]:
                                follow[1].append(simbolos[j + 1])
                    elif self.esNoTerminal(simbolos[j + 1]):
                        # Si el siguiente símbolo es un no terminal, añadimos su First al Follow del no terminal
                        for first in self.first:
                            if first[0] == simbolos[j + 1]:
                                for f in first[1]:
                                    if f != '&':
                                        for follow in self.follow:
                                            if follow[0] == simbolos[j]:
                                                if f not in follow[1]: # Evita duplicados
                                                    follow[1].append(f)
                elif self.esNoTerminal(simbolos[j]) and j == len(simbolos) - 1:
                    # Si es el último símbolo y es un no terminal, añadimos el Follow del no terminal
                    for follow in self.follow:
                        if follow[0] == simbolos[j]:
                            for f in self.follow:
                                if f[0] == lado_izquierdo and f[0] != simbolos[j]:
                                    if f[1] not in follow[1]:  # Evita duplicados
                                        follow[1].extend(f[1])
    
    def obtenerNoTerminal(self, produccion):
        inicio = 0
        fin = 0
        while inicio < len(produccion) and produccion[inicio] != '<':
            inicio += 1

        while fin < len(produccion) and produccion[fin] != '>':
            fin += 1
        
        return produccion[inicio:fin+1]  # Devuelve el no terminal encontrado en la producción
    
    def obtenerPrimerSimbolo(self, derivacion):
        inicio = 0
        fin = 0

        while fin < len(derivacion) and derivacion[fin] != ' ':
            fin += 1
        
        return derivacion[inicio:fin]  # Devuelve el no terminal encontrado en la producción


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
    
    def printFirst(self):
        for no_terminal, simbolos in self.first:
            print(f"First({no_terminal}): {', '.join(simbolos)}")

    def main(self):
        self.calcularFirst()
        #self.calcularFollow()
        #self.calcularMatriz()
        self.printFirst()
        #print("Follow:", self.follow)
        #print("Matriz Predictiva:", self.matrix)    
    
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

if __name__ == "__main__":
    FirstFollowMatrix().main()
