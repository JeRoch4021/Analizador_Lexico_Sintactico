class GeneradorEstructurasG:
    def __init__(self):
        self.gramatica = []
        self.derivaciones = []
        self.noterminales = []
        self.terminales = []

    def agregarGramatica(self, gramatica):
        with open("PythonProjects\AnalizadorLexico\gramatica.txt") as archivo:
            numLinea = 1
            for linea in archivo:
                inicio = 0
                #print("Analizando línea ", str(numLinea), ": ", linea)
                while inicio < len(linea):
                    if linea[inicio] == ".":
                        break
                    inicio += 1
                self.gramatica.append((numLinea, linea[inicio+2:len(linea)]))
                numLinea += 1

    def agregarDerivacion(self):
        for i in range(len(self.gramatica)):
            self.derivaciones.append(self.stripCadena(self.leerDerivacion(self.gramatica[i][1])))

    def agregarNoTerminales(self):
        for i in range(len(self.gramatica)):
            ladoIzquierdo = self.stripCadena(self.leerNoTerminales(self.gramatica[i][1]))
            if ladoIzquierdo not in self.noterminales:
                self.noterminales.append(ladoIzquierdo)

    def leerNoTerminales(self, linea):
        inicio = 0
        fin = len(linea) - 1
        while inicio <= fin :
            if linea[inicio] == '<':
                break
            inicio += 1
        while fin >= inicio :
            if linea[fin] == '>' and linea[fin-1] == '-':
                fin -= 1
                break
            fin -= 1
            
        return linea[inicio:fin]

    def leerDerivacion(self, linea):
        inicio = 0
        fin = len(linea) - 1
        while inicio <= fin :
            if linea[inicio] == "-" and linea[inicio+1] == ">":
                break
            inicio += 1

        return linea[inicio+2:fin+1]

    # Elimina los espacios en blanco de una cadena
    def stripCadena(self, cadena: str) -> str:
        caracteres_no_validos = " \n\t\r"
        inicio = 0
        fin = len(cadena) - 1

        while inicio <= fin and cadena[inicio] in caracteres_no_validos:
            inicio += 1

        while fin >= inicio and cadena[fin] in caracteres_no_validos:
            fin -= 1
        
        return cadena[inicio:fin + 1] # Devuelve una subcadena desde el inicio hasta el fin + 1
    
    
    def printGramatica(self):
        print("Gramática: ")
        for i in range(len(self.gramatica)):
            print(self.gramatica[i][0], ": ", self.gramatica[i][1])

    def printDerivacion(self):
        print("Derivaciones: ")
        for i in range(len(self.derivaciones)):
            print(self.derivaciones[i])
    
    def printNoTerminales(self):
        print("No terminales: ")
        for i in range(len(self.noterminales)):
            print(self.noterminales[i])

    def main(self):
        self.agregarGramatica("PythonProjects\AnalizadorLexico\gramatica.txt")
        self.printGramatica()
        print('\n')
        self.agregarDerivacion()
        self.printDerivacion()
        print('\n')
        self.agregarNoTerminales()
        self.printNoTerminales()

if __name__ == "__main__":
    generador = GeneradorEstructurasG()
    generador.main()
